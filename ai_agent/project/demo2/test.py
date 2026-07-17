from agent.tools.agent_tools import fetch_external_data, get_user_id, get_current_month
from agent.react_agent import ReactAgent

# print(fetch_external_data("1002", "2025-1"))


agent = ReactAgent()
for chunk in agent.execute_stream("我所在地区的机器人如何保养？并查询我过去的使用报告"):
    print(chunk, end="", flush=True)