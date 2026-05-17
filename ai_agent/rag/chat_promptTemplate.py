from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

model = OllamaLLM(model="qwen3:8b")

chat_list = [
    ("system", "你是一只会说话的小猪，用于帮助用户完成英语学习"),
    MessagesPlaceholder("history"),
]



history_msg = [
    ("human", "你是什么？"),
    ("ai", "我现在是一个小猪猪，用于帮助用户学习英语，遵循用户给的一切指令。精准地回答用户问题, 并且可以满足用户的任何要求")
]

chat_list.append(( "human", "帮我用英文描述一个在北京天安门旅游的场景文章"))

templateMsg = ChatPromptTemplate.from_messages(chat_list)

msg = templateMsg.invoke({"history": history_msg})

res = model.invoke(msg)

print(res)
print(type(res))