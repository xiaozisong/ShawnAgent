import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

# 从 .env 读取 API 配置
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "glm-5.2"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL", "https://88.api456.me/v1"),
)

# 定义获取天气的方法
def get_weather(city: str) -> str:
  """获取给定城市的天气情况."""
  return f"该城市：{city}的天气是晴朗的！"

agent = create_agent(
  model=llm,
  tools=[get_weather],
  system_prompt="你是一个天气预报员，请根据用户的问题获取天气情况。",
)

result = agent.invoke(
  {"messages": [{ "role": "user", "content": "北京今天的天气怎么样？" }]}
)

print(result["messages"][-1].content_blocks)