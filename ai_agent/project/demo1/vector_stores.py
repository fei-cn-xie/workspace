from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
        """
        :param embedding: 向量嵌入模型
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory)
        
    def get_retriver(self):
        """
        返回向量检索器，方便加入chain
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == "__main__":
    from langchain_community.embeddings import OllamaEmbeddings, DashScopeEmbeddings
    # 获取 embedding 模型对象
    emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")
    retriver = VectorStoreService(embedding=emb).get_retriver()
    res = retriver.invoke("小红喜欢誰")
    print(res)
