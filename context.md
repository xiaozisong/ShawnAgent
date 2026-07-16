# 项目背景与学习上下文 (Context)

> 这份文档是 AI 助手在每次对话开始时必读的"长期记忆"。
> 它告诉助手：这个项目是什么、用户是谁、目标是什么、当前进度在哪里。
> 每次开会话时，AI 助手应当首先读取本文档，确保上下文一致。

---

## 一、用户画像

- **背景**：前端开发者，没有任何后端 + Agent 开发经验
- **熟悉**：TypeScript、JavaScript、async/await、REST API、组件化思维
- **不熟悉**：Python、SQLAlchemy、FastAPI、LangGraph、LLM 应用架构
- **目标**：通过本项目真正动手实现一个 Agent 应用，**边学 Agent 边学 Python**

## 二、学习参照的"答案项目"

- **路径**：`/Users/xiaozisong/Desktop/meme-mind-app-memeskill-0702/`
- **项目名**：MemeSkill（包名 `aegra`）
- **类型**：自托管的 AI Agent 后端，专注于智能写作助手场景
- **核心技术栈**：
  - LangGraph 1.0+（Agent 编排框架，核心）
  - LangChain 1.2+ / langchain-core 1.2+（LLM 抽象层）
  - langchain-openai / langchain-anthropic / langchain-google-genai（多模型支持）
  - deepagents 0.5.1（LangChain 官方深度 Agent 库，本项目本地打包在 `src/deepagents/`）
  - FastAPI（Web 框架）
  - PostgreSQL + SQLAlchemy + Alembic（持久化 + ORM + 迁移）
  - langgraph-checkpoint-postgres（Agent 状态持久化）
  - Langfuse（可观测性）
  - Uvicorn（ASGI 服务器）
- **关键目录结构**：
  - `src/agents/main_agent.py` — 主 Agent（MemeSkill_agent），600+ 行
  - `src/agents/game_design_workflow_agent.py` — 子 Agent
  - `src/tools/` — 11 个工具，含 think_tool、web_search_tool 等
  - `src/middleware/` — 15 个中间件，业务深度耦合
  - `src/agent_server/` — FastAPI 服务端
  - `src/deepagents/deepagents/graph.py` — `create_deep_agent` 工厂函数
  - `docs/` — 20 篇技术文档
  - `aegra.json` — Agent Graph 注册清单

## 三、学习项目（用户工作区）

- **路径**：`/Users/xiaozisong/Desktop/Agent/learning-agent/`
- **设计原则**：
  1. 不空学理论——每个知识点都有可运行代码
  2. 对照答案项目——学完每步能回头看 MemeSkill 对应代码
  3. 小步快跑——每步都能跑起来看到结果
  4. Python + Agent 同步学——知识点搭配，不割裂
- **里程碑路线**：

| # | 文件 | 主题 | Python 知识点 | Agent 知识点 | 对应答案项目代码 |
|---|------|------|-------------|------------|----------------|
| 1 | `m01_first_agent.py` | 第一个 Agent | 类型注解、函数、async | LLM 调用、Message、StateGraph | `deepagents/graph.py`、`model/__init__.py` |
| 2 | `m02_tool_agent.py` | 给 Agent 加工具 | 装饰器、docstring | Tool、Tool Message、循环 | `src/tools/think_tool.py` |
| 3 | `m03_memory_agent.py` | 让 Agent 有记忆 | list/dict 操作 | Chat History、State | `deepagents/middleware/memory.py` |
| 4 | `m04_stream_agent.py` | 流式响应 | yield、async generator | Streaming、SSE | `agent_server/api/runs.py` |
| 5 | `m05_fastapi_agent.py` | FastAPI 暴露 API | class、Pydantic | REST API、Middleware | `agent_server/main.py` |
| 6 | `m06_db_agent.py` | 数据库持久化 | SQLAlchemy | Checkpoint、Thread | `agent_server/services/` |
| 7 | `m07_multi_agent.py` | 多 Agent 协作 | 设计模式 | Sub-agent、Graph 嵌套 | `deepagents/middleware/subagents.py` |

## 四、当前进度

| 里程碑 | 状态 | 备注 |
|--------|------|------|
| 环境准备 | ⏳ 进行中 | 用户需要装 Homebrew、Python 3.12、uv |
| 里程碑 1 | ✅ 已创建 | `m01_first_agent.py` 已写完，等待用户运行 |
| 里程碑 2-7 | 🔲 未开始 | 等用户跑通里程碑 1 后再写 |

## 五、AI 助手行为约定

每次对话时，AI 助手应该：

1. **先读这份文档**，了解用户是谁、目标是什么、到哪一步了
2. **用中文回答**（用户已设置该规则）
3. **不要急于推进**：用户是前端转后端的初学者，需要解释清楚每个概念
4. **多用 TS ↔ Python 对照**：用户的支点是 TypeScript
5. **对照答案项目**：写新代码时明确告诉用户"这段对应 MemeSkill 里的哪个文件"
6. **代码注释要饱满**：学习项目的代码，注释比答案项目更详细
7. **小步验证**：每个里程碑都能独立运行，给用户正反馈
8. **遇到用户提问时判断**：
   - 是 Python 语法问题？→ 用 TS 类比解释
   - 是 Agent 概念问题？→ 用 MemeSkill 里的代码做对照
   - 是项目结构问题？→ 直接读答案项目源码确认
9. **不要主动写里程碑 N+1 的代码**，除非用户明确说"跑通了，继续"或"给我里程碑 X"

## 六、关键路径速查

```bash
# 答案项目
/Users/xiaozisong/Desktop/meme-mind-app-memeskill-0702/

# 学习项目
/Users/xiaozisong/Desktop/Agent/learning-agent/

# 跑第一个里程碑
cd /Users/xiaozisong/Desktop/Agent/learning-agent
cp .env.example .env       # 编辑填入 OPENAI_API_KEY
uv sync
uv run python m01_first_agent.py
```

## 七、变更日志

- **2026-07-15**：创建学习路线，完成里程碑 1 文件 `m01_first_agent.py`，将 `learning-agent/` 从答案项目目录移动到 `~/Desktop/Agent/` 用于独立学习
