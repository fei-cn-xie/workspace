from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableSerializable, RunnableSequence
from langchain_core.output_parsers import StrOutputParser


model = OllamaLLM(model="qwen3:8b")

prompt = ChatPromptTemplate([
    ("system", "你是一个英语老师，帮助用户完成英语学习。当用户询问单词时，不要生成过多的内容，尽最大可能精简回答"),
    MessagesPlaceholder("history"),
    ("human", "瓶子的英文是什么？")
])

chain = prompt | model 



history_msg = [
    ("human", "盒子的英文是什么？"),
    ("ai", "盒子=box")
]

print("prompt invoke: ", type(prompt.invoke({"history": history_msg})))
print("model invoke type: ", type(chain.invoke({"history": history_msg})))
print("chain type: ", type(chain))

print(chain.invoke({"history": history_msg}))

# 使用StrOutputParser-字符串输出解析器

output_parsers = StrOutputParser()

chain = chain | output_parsers | model

print(chain.invoke({"history": history_msg}))

