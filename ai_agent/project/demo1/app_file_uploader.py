"""
基于Streamlit完成web网页上传服务
pip install streamlit
"""

import streamlit as st

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
    st.write(text)
