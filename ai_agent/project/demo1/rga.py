from ast import mod

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough



def format_document(docs: list[Document]):
    if not docs:
        return "无参考资料"
    formated_str = ""
    for doc in docs:
        formated_str += f"文档片段：{doc.page_content}; 文档元数据: {doc.metadata}"
    
    return formated_str

class RagService(object):
    def __init__(self, embedding_model, chat_model):
        self.vector_store = VectorStoreService(
            embedding=embedding_model
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "通过参考资料，简洁专业地回答用户问题。参考资料：{context}"),
                ("user", "请回答用户提问：{input}"),
            ]
        )
        self.model = chat_model
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriver = self.vector_store.get_retriver()
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriver | format_document
            } | self.prompt_template | self.model | StrOutputParser()
        )
        return chain
    

if __name__ == "__main__":
    from langchain_community.embeddings import OllamaEmbeddings, DashScopeEmbeddings
    # 获取 embedding 模型对象
    emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")
    from langchain_ollama import OllamaLLM
    model = OllamaLLM(model="qwen3:8b")
    rs = RagService(embedding_model=emb, chat_model=model)

    res = rs.chain.invoke("小明喜欢谁？")
    print(res)
