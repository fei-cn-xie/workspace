from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.config import RunnableConfig
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

model = OllamaLLM(model="qwen3:8b")

prompt = PromptTemplate.from_template(
    "你是一个智能的助手, 你拥有一些历史消息: {chat_history}. 现在你根据用户输入回答用户"
    "用户的输入是{input}。 "
)

chain = prompt | model

chat_history_store = {}

def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

conversation_chain = RunnableWithMessageHistory(
    chain, # 被附加历史消息的Runnable, 通常是chain
    get_history,  # 获取指定会话id的历史会话函数
    input_messages_key="input", # 声明用户输入在模板中的占位符
    history_messages_key="chat_history" # 声明历史消息在模板中的占位符
)

session_config = {"configurable" : {"session_id" : "chat_001"}} # 格式固定

print(conversation_chain.invoke({"input": "小明有9条狗"}, session_config ) )
print(conversation_chain.invoke({"input": "Jack有3条狗"}, session_config ) )
print(conversation_chain.invoke({"input": "小明和Jack一共有几条狗？"}, session_config ) )


