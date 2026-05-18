from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.base import RunnableSerializable, RunnableSequence, RunnableLambda


model = OllamaLLM(model="qwen3:8b")


prompt = PromptTemplate.from_template("给我写一首{type}诗")

my_parser = RunnableLambda(print)

chain = prompt | model | my_parser 

chain.invoke(input={"type": "边塞"})

print("====================================")

my_parser2 = RunnableLambda(lambda content : {"content" : content})
chain = prompt | model | my_parser2
res = chain.invoke(input={"type": "边塞"})

print("res = ", res)