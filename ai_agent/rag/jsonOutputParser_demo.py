from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.base import RunnableSerializable, RunnableSequence

model = OllamaLLM(model="qwen3:8b")

first_prompt = PromptTemplate.from_template(
    "我姓:{lastname}, 生了个{gender}, 帮我给孩子取个名，并封装为json格式返回给我"
    "要求key是name, value是起的名。"
    "请严格遵守格式要求, 无任何多余字符串"
)

json_parser = JsonOutputParser()

chain = first_prompt | model
print( "============= start up ======== ")

data = {"lastname": "谢", "gender": "儿子"}

output = chain.invoke(data)


print("first_prompt | model -> ", type(output), " value = ", output)

print( "=================================")

chain = chain | json_parser

print("jsonparse type is -> ", type(chain), " value = ", chain)

print( "=================================")

second_prompt = PromptTemplate.from_template(
    "名字是{name}, 请解析其含义"
)

chain = chain | second_prompt

print("second prompt is = ", chain)

print( "=================================")

chain = chain | model

print("result : ", chain.invoke(data))



