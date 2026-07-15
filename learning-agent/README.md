# 边学边练：从零搭建 Agent 应用

这是一个为**前端开发者**设计的学习路径，目标是通过 7 个里程碑，让你从零开始搭建一个完整的 Agent 应用，**同时掌握 Python 和 LangGraph**。

## 学习理念

- **不空学理论**：每个知识点都配一段可运行代码
- **对照本仓库**：每学完一个里程碑，回头看 `src/` 里的对应代码
- **小步快跑**：每步都能跑起来看到结果，正反馈强
- **Python + Agent 同步学**：知识点搭配学，不会割裂

---

## 第 0 步：搭建 Python 开发环境（新 Mac 从零开始）

你当前的系统：macOS，Python 3.9.6（系统自带，版本太旧）

**注意**：不要卸载系统 Python！macOS 依赖它。我们需要安装一个独立的新版本。

### 安装 Homebrew（macOS 的包管理器，类似 npm install 装全局工具）

打开终端（Terminal.app），粘贴以下命令：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

过程中会要求你输入 Mac 密码，这是正常的。安装完成后会提示你执行两条命令把 brew 加入 PATH，按终端提示操作即可。

验证安装：

```bash
brew --version
# 输出类似: Homebrew 4.x.x
```

### 安装 Python 3.12

```bash
brew install python@3.12
```

安装完成后：

```bash
python3 --version
# 应该输出: Python 3.12.x
```

确认用的是新安装的 Python（而不是系统那个 3.9）：

```bash
which python3
# 应该输出: /opt/homebrew/bin/python3
# 而不是: /usr/bin/python3
```

如果还是 `/usr/bin/python3`，执行：

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
which python3  # 现在应该是 /opt/homebrew/bin/python3
```

### 安装 uv（Python 的 "npm"）

```bash
# 方法一：通过 pip（你刚装了 Python 3.12，有最新的 pip）
pip3 install uv

# 方法二：直接安装（更快）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证：

```bash
uv --version
```

### 准备一个 LLM API Key

学习阶段推荐用 OpenAI 的 API：

1. 访问 https://platform.openai.com/api-keys
2. 创建一个 API Key
3. 选择模型 `gpt-4o-mini`（最便宜，几块钱能用很久）

### 安装依赖 & 跑第一个程序

```bash
# 进入学习目录
cd learning-agent/

# 复制环境变量配置
cp .env.example .env

# 编辑 .env，填入你的 OPENAI_API_KEY
vim .env  # 或直接用编辑器打开

# 安装依赖（相当于 npm install）
uv sync

# 跑第一个里程碑
uv run python m01_first_agent.py
```

---

## 学习路线总览

| # | 主题 | Python 知识点 | Agent 知识点 | 对本项目代码 |
|---|------|--------------|-------------|-------------|
| 1 | 第一个 Agent | 变量/类型注解/函数 | LLM 调用、Message | `deepagents/graph.py` |
| 2 | 给 Agent 加工具 | 装饰器、docstring | Tool、Tool Message | `src/tools/think_tool.py` |
| 3 | 让 Agent 有记忆 | list/dict 操作 | Chat History、State | `deepagents/middleware/memory.py` |
| 4 | 流式响应 | async/await、yield | Streaming、SSE | `agent_server/api/runs.py` |
| 5 | 用 FastAPI 暴露 API | class、Pydantic | REST API、Middleware | `agent_server/main.py` |
| 6 | 数据库持久化 | SQLAlchemy、async | Checkpoint、Thread | `agent_server/services/` |
| 7 | 多 Agent 协作 | 设计模式 | Sub-agent、Graph | `deepagents/middleware/subagents.py` |

## 学习节奏建议

- **里程碑 1-2**：1-2 天，建立直觉
- **里程碑 3-4**：2-3 天，理解状态和流
- **里程碑 5-6**：3-4 天，搭出真正的后端
- **里程碑 7**：2-3 天，做出复杂 Agent

总计 **8-14 天**可以走完，每天 2-4 小时。

## 每个里程碑的文件

```
learning-agent/
├── m01_first_agent.py      # 里程碑 1 — 你的第一个 Agent
├── m02_tool_agent.py       # 里程碑 2 — 给 Agent 装工具
├── m03_memory_agent.py     # 里程碑 3 — Agent 有记忆了
├── m04_stream_agent.py     # 里程碑 4 — 流式输出
├── m05_fastapi_agent.py    # 里程碑 5 — Agent 做成 API
├── m06_db_agent.py         # 里程碑 6 — 持久化
├── m07_multi_agent.py      # 里程碑 7 — 多 Agent 协作
├── pyproject.toml          # 依赖配置
├── .env.example            # 环境变量模板
└── README.md               # 你正在看的
```

## 关键对照表：TypeScript ↔ Python

| TypeScript | Python |
|-----------|--------|
| `let x: number = 1` | `x: int = 1` |
| `interface Foo { a: string }` | `class Foo(BaseModel): a: str` |
| `async function f() {}` | `async def f(): ...` |
| `await f()` | `await f()` |
| `Promise.all([a, b])` | `asyncio.gather(a, b)` |
| `export default f` | 无显式 export，靠 `__all__` |
| `import { x } from 'y'` | `from y import x` |
| `npm init` | `uv init` |
| `npm install` | `uv sync` / `uv add` |
| `npm run xxx` | `uv run python xxx.py` |

开始吧 → `m01_first_agent.py`
