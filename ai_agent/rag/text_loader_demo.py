from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="ai_agent\\rag\\data\\stu.txt",
    encoding="utf-8"
)

document = loader.load()

print(document)
print("*="*30)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=509, # 分段的最大字符数
    chunk_overlap=50, # 分段之间允许重叠的字符数
    separators=["\n\n", "\n", ".", "。", "?", "!", "！", "？", " ", ":\n"], # 文本分段依据
    length_function=len, # 字符统计依据(函数)
)

split_docs = splitter.split_documents(document)

for sd in split_docs:
    print(sd)
    print("="*20)


