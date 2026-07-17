"""
yaml
"""

from re import S

import yaml
from utils.path_tool import get_abs_path

# RAG配置
def load_rag_config(config_path: str=get_abs_path("config/rag.yaml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# 向量数据库配置
def load_chroma_config(config_path: str=get_abs_path("config/chroma.yaml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 提示词配置
def load_prompts_config(config_path: str=get_abs_path("config/prompts.yaml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# Agent配置
def load_agent_config(config_path: str=get_abs_path("config/agent.yaml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()

if __name__ == "__main__":
    print(rag_config["chat_model_name"])