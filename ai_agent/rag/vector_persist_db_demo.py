from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader


# 获取 embedding 模型对象
emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")

vector_store = Chroma(
        collection_name="test_name", # 类似数据库表名
        embedding_function=emb, # 指定文本-向量模型
        persist_directory="ai_agent\\rag\\chroma_data" # 指定数据存放的文件夹
    )
loader = PyPDFLoader(
    file_path="ai_agent\\rag\\data\\fiction.pdf",
    mode="page", # 安装页进行划分Document对象
    # password="123" # 文档密码
)

doc = loader.load()

print("doc = " , doc)
print("+=*" * 20)

# 添加文档到向量数据库，并指定id
vector_store.add_documents(documents=doc)

# 相似性搜索, 4代表结果个数
similar_docs = vector_store.similarity_search(
    "三百万信用点", 
    1,
    filter={"source": "黑马"}) #  过滤内容
print(similar_docs)
