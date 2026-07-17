from calendar import month
import os

from langchain_core.tools import tool
from utils.logger_handler import logger
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_config
from utils.path_tool import get_abs_path


rag = RagSummarizeService()

external_data = {}

@tool(description="从向量数据库中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市的天气")
def get_weather(city: str):
    return f"城市{city}天气为晴天， 气温26摄氏度, 空气湿度为50%"

@tool(description="获取用户所在城市的名称")
def get_user_location():
    return "北京"

@tool(description="获取用户的id")
def get_user_id():
    user_ids = ["10" + f"{(i + 1):02d}" for i in range(10)]
    return random.choice(user_ids)

@tool(description="获取当前月份")
def get_current_month():
    month = ["2025-" + f"{(m + 1):02d}" for m in range(12)]
    return random.choice(month)

@tool(description="从外部系统中获取指定用户在指定月份的使用记录")
def fetch_external_data(user_id: str, month: str):
    """
    {
        "user_id": {
            "month": {
                "特征": xxx,
                "效率" xxx
            }
        }
    }
    """
    if not external_data:
       external_data_path = get_abs_path(agent_config["external_data_path"])
       if not os.path.exists(external_data_path):
           raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")
       
       with open(external_data_path, "r", encoding="utf-8") as f:
           for line in f.readlines()[1:]:
                arr = line.strip().split(",")
                user_id_t = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id_t not in external_data:
                    external_data[user_id_t] = {} 
                external_data[user_id_t][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }

    try:
        return external_data[user_id][month]
    except KeyError as e:
        logger.warning(f"[generate_external_data]未能检索到{user_id}在{month}的使用数据")
        
@tool(description="没有入参、没有返回值, 调用后触发中间件自动为场景注入上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"


if __name__ == "__main__":
    print(get_user_id())
    # print(generate_external_data(get_user_id(), get_current_month()))