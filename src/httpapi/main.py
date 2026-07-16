# 实现异步函数调用 HTTP API 
import httpx
import asyncio

async def fetch_weather(city: str) -> str:
    """异步调用 wttr.in 天启 API"""
    url = f"https://wttr.in/{city}?format=j1"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        weather = data["current_condition"][0]["weatherDesc"][0]["value"]
        temp = data["current_condition"][0]["temp_C"]
        return f"{city} 天气: {weather}, {temp}℃"

result = asyncio.run(fetch_weather("北京"))
print(result)