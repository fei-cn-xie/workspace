from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from sympy import content


model = ChatOllama(model="qwen3:8b")



@tool(description="查询AI消息")
def get_ai_news():
    return "AI is booming"

agent = create_agent(
    model=model,
    tools=[get_ai_news],
    system_prompt="你是一个聊天助手",
    # debug=True,
)




for chunk in agent.stream({
            "messages": [{"role":"user", "content": "Search the AI news, and summarize the findings"}]
        },stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")