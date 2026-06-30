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
        """
        获取已经存在的消息
        """
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
    
    # 添加消息
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

def get_history(session_id):
    return FileChatMsgHistory(session_id, ".\\ai_agent\\project\\demo1\\chat_history")