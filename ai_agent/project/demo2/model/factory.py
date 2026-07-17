from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_ollama import OllamaLLM, ChatOllama
from utils.config_handler import rag_config

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseLanguageModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseLanguageModel]:
        return ChatOllama(model=rag_config["chat_model_name"])
    

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseLanguageModel]:
        return OllamaEmbeddings(model=rag_config["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()