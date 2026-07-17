from urllib import response

from agent.react_agent import ReactAgent
import streamlit as st
"""
启动： streamlit run app_qa.py
"""

# 标题
st.title("智能扫地机器人客服")
# 分隔符
st.divider()

# 状态记录
if "agent" not in st.session_state:
    st.session_state['agent'] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state['message']:
    st.chat_message(message['role'],).write(message['content'])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({
        "role": "user",
        "content": prompt
    })
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state['agent'].execute_stream(prompt)
        response_messages = []
        def capture(generator, catch_list):
            for chuck in generator:
                catch_list.append(chuck)
                yield chuck
        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state['message'].append({
            "role": "assistant",
            "content": response_messages[-1]
        })
        st.rerun()



