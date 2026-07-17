
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call, dynamic_prompt, ModelRequest
from langchain.agents.middleware.types import AgentState
from langgraph.runtime import Runtime
from langgraph.prebuilt.tool_node import ToolCallRequest
from collections.abc import Awaitable, Callable, Sequence
from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompts, load_report_prompts
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    SystemMessage,
    ToolMessage,
)

from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Generic,
    Literal,
    Protocol,
    cast,
    overload,
)

from langgraph.types import Command

# 工具执行的监控
@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]],
    ) -> ToolMessage | Command[Any]:
    """
    工具执行的监控
    Args:
        request: 请求的数据封装
        handler: 执行的函数本身
    """
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入的参数：{request.tool_call['args']}")
    
    try:
        result = handler(request)
        logger.info(f"[tool monitor] {request.tool_call['name']} 工具调用成功")
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context['report'] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败, 原因{str(e)}")
        raise e

    

# 在模型执行前输出日志
@before_model
def log_before_model(
    state: AgentState,  # 整个Agent智能体中的状态记录
    runtime: Runtime, # 记录了整个执行过程中的上下文信息
):
    logger.info(f"[log_before_model]即将调用模型, 带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model] {type(state["messages"][-1]).__name__} | {state["messages"][-1].content.strip()}")
    return None

# 动态切换提示词
@dynamic_prompt # 每一次在生成提示词之前调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:  # 返回报告生成场景的提示词
        return load_report_prompts()
    return load_system_prompts()