from langchain.agents import create_agent, AgentState
from langgraph.runtime import Runtime
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool


model = ChatOllama(model="qwen3:8b")

@tool(description="获取天气")
def get_weather() -> str:
    return "雨夹雪"


"""
1. agent执行前
2. agent执行后
3. 模型执行前
4. 模型执行后
5. 工具执行中
6. 模型执行中
"""

# 1. agent执行前
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    # agent执行前会调用本函数， 并传入state 和runtime
    print(f"[before_agent] agent启动 附带{len(state["messages"])}条消息")


@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    # agent执行前会调用本函数， 并传入state 和runtime
    print(f"[after_agent] agent执行完毕 附带{len(state["messages"])}条消息")


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    # agent执行前会调用本函数， 并传入state 和runtime
    print(f"[before_model] 模型启动 附带{len(state["messages"])}条消息")


@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    # agent执行前会调用本函数， 并传入state 和runtime
    print(f"[after_model] model执行完毕 附带{len(state["messages"])}条消息")

@wrap_tool_call
def log_tool_call(request, handler):
    print("工具调用-----------")
    return handler(request)


@wrap_model_call
def log_model_call(request, handler):
    print("模型调用-----------")
    return handler(request)


agent = create_agent(
    model=model,
    tools=[get_weather],
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, log_tool_call, log_model_call],
    system_prompt="你是一个聊天助手，必须严格遵守[思考 ==> 行动 ==> 观察 ==> 再思考]的流程解决问题。同时需要告知用户思考过程，工具调用原因，按照思考、行动、观察三个结构告知用户",
    # debug=True,
)

for chunk in agent.stream({
            "messages": [{"role":"user", "content": "北京天气怎么样？"}]
        },stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"{latest_message.__class__.__name__} : {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")