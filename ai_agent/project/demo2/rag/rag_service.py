"""
总结服务类: 用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""

from langchain_core.output_parsers import StrOutputParser
from model.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from rag.vector_store import VectorStoreService
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriver = self.vector_store.get_retriver()
        self.promt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.promt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain
    
    def retriver_docs(self, query: str) -> list[Document]:
        return self.retriver.invoke(query)
    
    def rag_summarize(self, query:str) -> str:
        context_docs = self.retriver_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据： {doc.metadata}\n"
        return self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )