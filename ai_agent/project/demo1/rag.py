from ast import mod

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda



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
                ("system", "并且我提供的与用户的会话记录如下: "),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}"),
            ]
        )
        self.model = chat_model
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriver = self.vector_store.get_retriver()

        def format_for_retriver(value: dict) -> str:
            # 自定义函数实现参数修正，从而兼容官方代码
            print("-------", value)
            return value["input"]
        
        def format_for_prompt_template(value: dict):
            print("------temp2:", value)
            value["history"] = value["input"]["history"]
            value["input"] = value["input"]["input"]
            print("======add history=====", value)
            return value
        
        def temp(value):
            print("==============", value)
            return value

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriver) |  retriver | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | RunnableLambda(temp) | self.model | StrOutputParser()
        )

        enhanced_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input", # 用户输入占位
            history_messages_key="history" # 历史消息占位
        )

        print("ok================")

        # 增强链
        return enhanced_chain
    
    

if __name__ == "__main__":
    from langchain_community.embeddings import OllamaEmbeddings, DashScopeEmbeddings
    # 获取 embedding 模型对象
    emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")
    from langchain_ollama import OllamaLLM
    model = OllamaLLM(model="qwen3:8b")
    rs = RagService(embedding_model=emb, chat_model=model)

    # session id配置
    session_config = {
        "configurable": {
            "session_id": "user001"
        }
    }

    res = rs.chain.invoke({"input": "刚刚我问了什么？"}, session_config)
    print(res)
