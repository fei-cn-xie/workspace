from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.pdf import PyPDFLoader

loader = CSVLoader(
    file_path="ai_agent\\rag\\data\\stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": ",", # 指定分隔符号
        "quotechar": '"',   # 指定带有分隔符文本的引号是单引号还是双引号
        "fieldnames": ['a','b','c','d'] #指定一个表头
    }
)


# 批量加载
documents = loader.load()

for doc in documents:
    print(type(doc), doc)


# 懒加载 .lazy_load()

for doc in loader.lazy_load():
    print(doc)