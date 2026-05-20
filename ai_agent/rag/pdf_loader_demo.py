from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="ai_agent\\rag\\data\\fiction.pdf",
    mode="page", # 安装页进行划分Document对象
    # password="123" # 文档密码
)

doc = loader.load()

print(doc)