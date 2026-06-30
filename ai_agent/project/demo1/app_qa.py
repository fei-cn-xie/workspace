import time

import streamlit as st
from rag import RagService
from langchain_community.embeddings import OllamaEmbeddings, DashScopeEmbeddings
from langchain_ollama import OllamaLLM

# 获取 embedding 模型对象
emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")
model = OllamaLLM(model="qwen3:8b")



st.title("智能客服")
st.divider() # 分隔符

# 命令行执行streamlit run app_qa.py运行

# 保证streamlit消息缓存。因为页面一刷新代码会重跑一遍，不设置缓存会导致内存数据丢失。
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你的?"}]

# 单例
if "ragService" not in st.session_state:
    st.session_state["ragService"] = RagService(embedding_model=emb, chat_model=model)

for msg in st.session_state["message"]:
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入栏
prompt = st.chat_input() 

if prompt:
    st.chat_message("user").write(prompt)

    st.session_state["message"].append( {"role": "user", "content": prompt})
    
    # session id配置
    session_config = {
        "configurable": {
            "session_id": "user001"
        }
    }

    ai_res_list = []
    with st.spinner("AI思考中..."):
        res_stream = st.session_state["ragService"].chain.stream({"input": prompt}, session_config)

        # 定义抓包工具方法，获取流式输出的全部内容
        def capture(generator, chache_list):
            for chunck in generator:
                chache_list.append(chunck)
                yield chunck
        

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})