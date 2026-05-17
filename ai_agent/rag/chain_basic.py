from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableSerializable, RunnableSequence

model = OllamaLLM(model="qwen3:8b")

chat_list = [
    ("system", "我是一个辅助谢飞完成英语学习的性感美丽有魅力的大姐姐，御姐风，严肃地教导谢飞完成英语学习"),
    MessagesPlaceholder("history"),
    ("human", "我不想学习了，我很浮躁")
]

chat_template = ChatPromptTemplate(chat_list)

history_msg = [
    ("human", "history是什么意思？"),
    ("ai", "history是历史的意思，亲爱的飞飞同学")
]

# 顺序必须是 prompt -> model, 实际等于 model.invoke(prompt.invoke(msg))

chain : RunnableSerializable = chat_template | model

print(type(chain))
res = chain.invoke({"history": history_msg})

print(res)