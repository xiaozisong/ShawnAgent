"""
=============================================================================
里程碑 1：第一个 Agent
=============================================================================
Python 知识点：变量、类型注解、函数、async/await、f-string
Agent 知识点：LLM 调用、Message 类型、最简单的 Graph

学习目标：
  1. 认识 Python 语法（类型注解、async/await）
  2. 理解 LLM 的输入和输出格式（HumanMessage → AIMessage）
  3. 理解为什么需要 LangGraph（状态管理）
  4. 能写出"Hello World"级别的 Agent

对照本仓库：src/deepagents/deepagents/graph.py 第 1-24 行的导入
           src/model/__init__.py 的 get_default_model
=============================================================================

Python 知识点速览（和 TS 对比）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TS: let name: str = "Alice"         → Python: name: str = "Alice"
  TS: function add(a: number, b) {}   → Python: def add(a: int, b: int) -> int: ...
  TS: async function f() { await g() } → Python: async def f(): await g()
  TS: `Hello ${name}`                → Python: f"Hello {name}"
  TS: import { x } from 'y'          → Python: from y import x
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ─── Python 知识点：导入模块 ──────────────────────────────────────────────
# Python 的 import 和 JS 很像：
#   from module import name  → 相当于 JS 的 import { name } from 'module'
#   import module            → 相当于 JS 的 import * as module
#   第三方库装在 site-packages，和 node_modules 类似
import os
from typing import Optional  # Python 3.10 后可用 X | None 代替

# dotenv 类似 JS 的 dotenv 或 cross-env，从 .env 文件加载环境变量
from dotenv import load_dotenv

# ─── LangChain 核心类型 ──────────────────────────────────────────────────
# HumanMessage = 用户发的消息（相当于你打字给 ChatGPT）
# AIMessage    = AI 回复的消息（相当于 ChatGPT 回复你）
# SystemMessage= 系统指令（相当于给 ChatGPT 的 system prompt）
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ChatOpenAI = 封装了 OpenAI API 的 LLM 对象
# 注意：它兼容任何 OpenAI 兼容的 API（包括本项目的火山引擎 Ark）
from langchain_openai import ChatOpenAI

# ─── LangGraph 核心 ──────────────────────────────────────────────────────
# StateGraph 是 Agent 的"骨架"，定义状态如何在节点间流动
# START/END 是图的固有节点，分别表示"开始"和"结束"
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.state import CompiledStateGraph

# ──────────────────────────────────────────────────────────────────────────
# 第 1 步：认识 Python 类型注解 + 一个简单的 async 函数
# ──────────────────────────────────────────────────────────────────────────

def greet(name: str, times: int = 1) -> str:
    '''Python 类型注解速览：
    
    - `name: str`     → 参数类型注解，相当于 TS 的 name: string
    - `times: int = 1` → 有默认值的参数，相当于 TS 的 times = 1
    - `-> str`        → 返回类型注解，相当于 TS 的 ): string {
    - `"""..."""`     → docstring，函数的文档说明（可以看到本仓库大量使用）
    - f"..."          → f-string，相当于 TS 的模板字符串 `...`
    '''
    return f"你好 {name}! " * times

# ─── Python 知识点：if __name__ == "__main__" ────────────────────────────
# 这是 Python 的"入口"写法，相当于：
#   if (require.main === module) { ... }
# 或者直接类比：这个 if 块就是"这个文件的 main 函数"
#
# 怎么运行：
#   cd learning-agent
#   uv run python m01_first_agent.py
#
# 第一次运行时，uv 会自动创建虚拟环境并安装依赖（类似 npm install 然后 node xxx.js）
if __name__ == "__main__":
    # ─── 载入 .env ──────────────────────────────────────────────────────
    # load_dotenv() 会读取项目根目录和当前目录下的 .env 文件
    # 相当于 JS 的: import 'dotenv/config'
    load_dotenv()

    # ─── Python 知识点：读取环境变量 ────────────────────────────────────
    # os.getenv("KEY", "default") 相当于 process.env.KEY || "default"
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    model_name: str = os.getenv("OPENAI_MODEL", "glm-5.2")
    base_url: str = os.getenv("BASE_URL", "https://88.api456.me/v1")

    if not api_key:
        print("=" * 60)
        print("⚠️  未设置 OPENAI_API_KEY")
        print("请复制 .env.example 为 .env 填入你的 API Key")
        print("获取地址: https://platform.openai.com/api-keys")
        print("=" * 60)
        exit(1)

    # ═════════════════════════════════════════════════════════════════════
    # 第一部分：最简单的 LLM 调用（这不是 Agent，但 Agent 的基础）
    # ═════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 60)
    print("📌 第 1 步：直接调用 LLM（还没有 Graph，但这是 Agent 的基础）")
    print("=" * 60)

    # ─── Python 知识点：创建对象 ────────────────────────────────────────
    # ChatOpenAI(model=..., api_key=...) 相当于 new ChatOpenAI(...)
    # Python 不需要 new 关键字
    llm = ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url)

    # ─── Python 知识点：调用 async 函数 ────────────────────────────────
    # langchain 的 .ainvoke() 是 async 函数，需要用 await 调用
    # 但 await 只能在 async def 内使用，所以我们用一个简单的方式：
    # 对于顶层代码，Python 提供了 asyncio.run() 来运行 async 函数
    
    # 我们先写一条消息发给 LLM
    # HumanMessage(content="...") 相当于 [{role: "user", content: "..."}]
    messages: list[HumanMessage] = [HumanMessage(content="用一句话解释什么是 Agent（智能体）")]

    # ─── Python 知识点：.invoke（同步）vs .ainvoke（异步）─────────────
    # 这个项目大量使用 async，因为要处理并发请求
    # 我们先用同步的 .invoke 体验一下（和 TS 不同，Python 里同步调用也是常见的）
    # 注意：ChatOpenAI 的 .invoke 会发起网络请求，会等待返回
    print("\n🔄 正在调用 LLM...")
    response: AIMessage = llm.invoke(messages)  # ← 这里会真的调 OpenAI API
    
    # ─── Python 知识点：f-string + 对象属性访问 ────────────────────────
    # 相当于: console.log(`回复: ${response.content}`)
    print(f"\n🤖 回复: {response.content}")
    print(f"📊 元数据: {response.response_metadata}")

    # ═════════════════════════════════════════════════════════════════════
    # 第 2 步：为什么需要 Graph？
    # ═════════════════════════════════════════════════════════════════════
    # 上面只是"一次调用"，不是 Agent。Agent 的特点是：
    # 1. 多次调用（LLM → 工具 → LLM → 工具 → ...）
    # 2. 每次调用的结果会影响下一次（有状态）
    # 3. 需要决定"下一步干什么"（路由逻辑）
    #
    # LangGraph 的 StateGraph 就是管理这个流程的框架。
    # 就像 React 需要管理组件状态一样，Agent 需要管理对话状态。
    
    print("\n" + "=" * 60)
    print("📌 第 2 步：用 StateGraph 构建最简 Agent")
    print("=" * 60)

    # ─── Python 知识点：Graph 的概念 ────────────────────────────────────
    # StateGraph 接受一个"状态 schema"，告诉框架"状态长什么样"
    #
    # MessagesState 是 LangGraph 内置的状态类型：
    #   {
    #     messages: list[BaseMessage]  ← 消息历史
    #   }
    #
    # 相当于 TS 的:
    #   interface State {
    #     messages: BaseMessage[]
    #   }

    # 创建一个 Graph 实例
    graph_builder: StateGraph = StateGraph(MessagesState)

    # ─── Python 知识点：定义节点函数 ───────────────────────────────────
    # 在 LangGraph 中，每个"节点"就是一个 Python 函数
    # 函数接收当前状态（state），返回更新后的状态
    #
    # 对照本仓库 src/deepagents/deepagents/graph.py 第 43 行：
    # 那个 BASE_AGENT_PROMPT 就是这里 system_prompt 的作用
    def call_llm(state: MessagesState) -> dict:
        """Graph 节点函数。
        
        Python 知识点：
        - `state: MessagesState`：类型注解，表示 state 是 MessagesState 类型
        - `-> dict`：返回类型是 dict（字典，相当于 JS 的 {}）
        - `state["messages"]`：访问字典的 key，相当于 JS 的 state.messages
          也可以用 state.get("messages", []) 更安全
        
        Args:
            state: 当前对话状态，包含 messages 列表
            
        Returns:
            更新后的状态（dict 格式，键名对应状态字段）
        """
        # 获取当前消息列表
        current_messages: list = state["messages"]
        
        # 调用 LLM
        # messages=current_messages 直接传入全部历史，LLM 就"知道上下文"
        # 这就是 Chat 类的工作原理
        result: AIMessage = llm.invoke(current_messages)
        
        # 返回更新：把 AI 的回复追加到消息列表
        # {"messages": result} 是简写，LangGraph 会自动处理追加
        # 完整写法是: {"messages": [result]}
        return {"messages": [result]}

    # 把函数注册为 Graph 的一个节点
    # 节点名 "llm" 可以任意取，但需要唯一
    graph_builder.add_node("llm", call_llm)

    # ─── Python 知识点：设置边（Edge） ─────────────────────────────────
    # 边定义"从哪里到哪里"
    # START → llm：图一开始，就进入 llm 节点
    # llm → END：llm 节点结束后，图结束
    #
    # 最简单的 Agent 就是：START → [调用 LLM] → END
    graph_builder.add_edge(START, "llm")
    graph_builder.add_edge("llm", END)

    # ─── 编译图 ─────────────────────────────────────────────────────────
    # .compile() 相当于 React 的 render：检查图结构合法性，返回可执行对象
    graph: CompiledStateGraph = graph_builder.compile()

    # ─── 用 Graph 运行 ──────────────────────────────────────────────────
    print("\n🔄 Graph 正在运行...")
    
    # graph.invoke() 接收初始状态，运行整个图
    # 输入: {"messages": [用户消息]}
    # 输出: {"messages": [用户消息, AI回复]}
    final_state: dict = graph.invoke({
        "messages": [HumanMessage(content="用一句话解释什么是 Graph（图）")]
    })

    # ─── Python 知识点：从结果中提取信息 ───────────────────────────────
    # final_state["messages"][-1] 取最后一条消息
    # Python 支持负索引：-1 是最后一个，-2 是倒数第二个
    # 相当于 JS 的 arr[arr.length - 1]
    last_message: AIMessage = final_state["messages"][-1]
    print(f"\n🤖 Graph 回复: {last_message.content}")

    # ═════════════════════════════════════════════════════════════════════
    # 第 3 步：加一个 System Prompt（系统提示词）
    # ═════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 60)
    print("📌 第 3 步：加系统提示词（System Prompt）")
    print("=" * 60)

    # SystemMessage 相当于给 ChatGPT 的"自定义指令"
    # 对照本仓库的 src/deepagents/deepagents/graph.py 第 43 行 BASE_AGENT_PROMPT
    system_prompt = SystemMessage(
        content="你是一个 Python 导师。请用简洁、易懂的方式解释概念。"
    )

    final_state_with_system: dict = graph.invoke({
        "messages": [
            system_prompt,  # ← 系统提示词排在前面
            HumanMessage(content="什么是 async/await？")  # ← 用户消息在后面
        ]
    })
    last_msg: AIMessage = final_state_with_system["messages"][-1]
    print(f"\n🤖 导师回复: {last_msg.content}")

    # ═════════════════════════════════════════════════════════════════════
    # 总结：你今天学到的 Python + Agent 知识
    # ═════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("📝 里程碑 1 总结")
    print("=" * 60)
    print("""
Python 知识点:
  ✅ 变量和类型注解: name: str = "hello"
  ✅ 函数定义: def add(a: int, b: int) -> int:
  ✅ f-string: f"Hello {name}"
  ✅ if __name__ == "__main__":  # 入口
  ✅ async/await 的概念
  ✅ 字典操作: state["key"]、.get()
  ✅ 列表负索引: arr[-1] 取最后一个
  ✅ import / from ... import

Agent 知识点:
  ✅ HumanMessage / AIMessage / SystemMessage
  ✅ ChatOpenAI 的基本调用
  ✅ StateGraph 的三个核心: State → Node → Edge
  ✅ START → [LLM Node] → END 是最简 Agent
  ✅ .compile() → .invoke() 是运行流程

下一步:
  → m02_tool_agent.py: 给 Agent 加上工具调用
""")
