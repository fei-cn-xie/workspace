from langchain_community.document_loaders import JSONLoader
import json

loader = JSONLoader(
    file_path="ai_agent\\rag\\data\\stu.json",
    jq_schema=".[].name",     # jq_schema的语法
    json_lines=False,   # 是否是jsonLines文件（每一行都是json的文件）
    text_content=True, # 抽取的是否是字符串
)

documents = loader.load()
print(documents)
