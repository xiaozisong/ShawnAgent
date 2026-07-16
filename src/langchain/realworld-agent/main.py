# 导入包
import os
import urllib.error
import urllib.request

from langchain.agents import create_agent
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
  model = os.getenv("OPENAI_MODEL", "glm-5.2"),
  api_key = os.getenv("OPENAI_API_KEY"),
  base_url = os.getenv("BASE_URL", "https://88.api456.me/v1"),
  temperature = 0.5,
  timeout = 600,
  streaming = True,
)

SYSTEM_PROMPT = """
你是一个文学数据助手。

## 能力

- `fetch_text_from_url`：从 URL 加载文档文本到对话中。
不要猜测行数或位置——必须基于已保存文件的工具结果来给出结论。
"""

@tool
def fetch_text_from_url(url: str) -> str:
  """
  从给定的URL中获取文本内容。
  """
  req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
  )
  try:
    with urllib.request.urlopen(req, timeout = 120) as resp:
      raw = resp.read()
  except urllib.error.URLError as e:
    return f"获取URL内容失败：{e}"
    text = raw.decode("utf-8", errors="replace")
    return text

# model = init_chat_model(
#   "gemini-3.1-pro-preview",
#   model_provider = "google-genai",
#   temperature = 0.5,
#   timeout = 600,
#   max_tokens = 25000,
#   streaming = True,
# )

checkpointer = InMemorySaver()

agent = create_agent(
  model = llm,
  tools = [fetch_text_from_url],
  system_prompt = SYSTEM_PROMPT,
  checkpointer = checkpointer,
)

deep_agent = create_deep_agent(
  model = llm,
  tools = [fetch_text_from_url],
  system_prompt = SYSTEM_PROMPT,
  checkpointer = checkpointer,
)

content = f"""
Project Gutenberg 收录了 F. Scott Fitzgerald 所著《了不起的盖茨比》的纯文本版本。
URL: https://www.gutenberg.org/files/64317/64317-0.txt

请尽可能回答以下问题：

1) 完整的 Gutenberg 文件中，有多少行包含子串 `Gatsby`（按行计数，而非行内的出现次数，每行以换行符结尾）。
2) 文件中第一个包含 `Daisy` 的行的行号（基于 1）。
3) 一段两句的中立摘要。

请尽力完成 (1) 和 (2)。如果在任何时刻你发现无法用现有工具和推理来**验证**确切答案，请不要编造数字：对该字段使用 `null`，并在 `how_you_computed_counts` 中说明限制。如果遇到任何错误，请报告错误内容及错误信息。
"""


agent_result = agent.invoke(
  {"messages": [{"role": "user", "content": content}]},
  config={"configurable": {"thread_id": "great-gatsby-lc"}},
)
deep_agent_result = deep_agent.invoke(
  {"messages": [{"role": "user", "content": content}]},
  config={"configurable": {"thread_id": "great-gatsby-da"}},
)

print(agent_result["messages"][-1].content_blocks)
print("\n")
print(deep_agent_result["messages"][-1].content_blocks)