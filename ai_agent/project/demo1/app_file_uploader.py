"""
基于Streamlit完成web网页上传服务
pip install streamlit

# 运行
streamlit run app_file_uploader.py

streamlit特点: 网页刷新会导致代码重跑一边。 存在的问题：会导致代码状态重置。比如全局变量等内容。
因此可以使用streamlit.session_state['key'] = value 能够记录状态，持续存在。

"""

import streamlit as st
from knowledge_base import KnowledgeBaseService


if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


st.title("知识库更新服务")

uploaded_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024
    st.subheader(f"文件名: {file_name}")
    st.write(f"格式:{file_type} | 大小:{file_size:.2f} KB")

    # get_value
    text = uploaded_file.getvalue().decode("utf-8")
    # st.write(text)
    with st.spinner("载入知识库中..."):
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)

