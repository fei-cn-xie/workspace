import json, os
from collections.abc import Sequence
from langchain_core.messages import messages_from_dict, message_to_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

class FileChatMsgHistory(BaseChatMessageHistory):
    
    def __init__(self, session_id, storage_path):
        self.storage_path = storage_path
        self.session_id = session_id

        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                os.path.join(self.storage_path, self.session_id),
                "r",
                encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
    
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages) # 已有的消息
        all_messages.extend(messages) # 新的消息
        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)
        
    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)



model = OllamaLLM(model="qwen3:8b")

prompt = PromptTemplate.from_template(
    "你是一个智能的助手, 你拥有一些历史消息: {chat_history}. 现在你根据用户输入回答用户"
    "用户的输入是{input}。 "
)

chain = prompt | model

chat_history_store = {}

def get_history(session_id):
    return FileChatMsgHistory(session_id, ".\\ai_agent\\rag")

conversation_chain = RunnableWithMessageHistory(
    chain, # 被附加历史消息的Runnable, 通常是chain
    get_history,  # 获取指定会话id的历史会话函数
    input_messages_key="input", # 声明用户输入在模板中的占位符
    history_messages_key="chat_history" # 声明历史消息在模板中的占位符
)

session_config = {"configurable" : {"session_id" : "chat_001"}} # 格式固定

# print(conversation_chain.invoke({"input": "tom今年有9条狗"}, session_config ) )
# print(conversation_chain.invoke({"input": "jerry去年有3条狗，死了2条狗，今年又买了1条狗"}, session_config ) )
print(conversation_chain.invoke({"input": "tom和jerry今年一共有几条狗？"}, session_config ) )
