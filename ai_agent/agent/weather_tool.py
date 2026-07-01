from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from sympy import content


model = ChatOllama(model="qwen3:8b")


@tool(description="查询天气")
def get_weather():
    return "晴天"

@tool(description="查询AI消息")
def get_ai_news():
    return "AI is booming"

agent = create_agent(
    model=model,
    tools=[get_weather, get_ai_news],
    system_prompt="你是一个聊天助手",
    # debug=True,
)

res = agent.invoke(
    {
        "messages": [
            {"role":"user", "content": "明天北京的天气如何呢？"}
        ]
    }
)

parser = StrOutputParser()

for msg in res["messages"]:
    print(f"{type(msg).__name__}: {parser.invoke(msg)}")

