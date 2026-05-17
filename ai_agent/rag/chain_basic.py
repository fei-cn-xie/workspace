from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableSerializable, RunnableSequence

model = OllamaLLM(model="qwen3:8b")

chat_list = [
    ("system", "我是一个辅助用户完成英语学习ai助手，教导用户完成英语学习, 每次的内容都是详细地回答"),
    MessagesPlaceholder("history"),
    ("human", "我不想学习了，我很浮躁")
]

chat_template = ChatPromptTemplate(chat_list)

history_msg = [
    ("human", "history是什么意思？"),
    ("ai", "history是历史的意思")
]

# 顺序必须是 prompt -> model, 实际等于 model.invoke(prompt.invoke(msg))

# | = def __or__ -> RunnableSerializable
chain : RunnableSerializable = chat_template | model

print(type(chain))
res = chain.invoke({"history": history_msg})

# print(res)


res = chain.stream({"history": history_msg})

for chunck in res:
    print(chunck, flush=True, end="")