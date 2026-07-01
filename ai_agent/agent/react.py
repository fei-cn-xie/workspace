from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from numpy import double
from sympy import content


model = ChatOllama(model="qwen3:8b")



@tool(description="获取用户身高(cm)")
def get_height():
    return 170

@tool(description="获取体重(kg)")
def get_weight():
    return 51

@tool(description="尺码推荐")
def suggest(height: float, weight: float):
    print(f"h: {height} , w : {weight}")
    return "L"


agent = create_agent(
    model=model,
    tools=[get_height, get_weight, suggest],
    system_prompt="你是一个聊天助手，必须严格遵守[思考 ==> 行动 ==> 观察 ==> 再思考]的流程解决问题。同时需要告知用户思考过程，工具调用原因，按照思考、行动、观察三个结构告知用户",
    # debug=True,
)




for chunk in agent.stream({
            "messages": [{"role":"user", "content": "根据用户的身高体重推荐尺码。"}]
        },stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"{latest_message.__class__.__name__} : {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")