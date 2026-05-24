from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = OllamaLLM(model="qwen3:8b")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的参考资料，极其简短且专业地回答用户的问题。参考资料：{context}。一切以提供的参考资料为准，不需要额外信息。"),
        ("system", "每一个回复加个可爱的人脸表情"),
        ("user", "用户提问: {input}")
    ]
)
# 获取 embedding 模型对象
emb= OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")
vector_store = InMemoryVectorStore(embedding=emb)

vector_store.add_texts(["减肥就是要少吃多练", "减肥饮食上只吃西兰花", "运动上只能跑步", "好好学习天天向上", "甜瓜不甜"])

input_text = "如何减肥？"

search_result = vector_store.similarity_search(input_text, 3)

reference_text = "["
for doc in search_result:
    reference_text += doc.page_content
reference_text  += "]"

def print_prompt(prompt):
    print(prompt)
    print("=" * 30)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser() | print_prompt

chain.invoke({"input": input_text, "context": reference_text})


