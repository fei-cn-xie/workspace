import os
from openai import OpenAI


client = OpenAI(
    api_key="ollama",
    base_url="http://127.0.0.1:11434/v1"
)

completion = client.chat.completions.create(
    model="qwen3:8b",
    messages=[{'role': 'user', 'content':'who you are?'}]
)
print(completion.choices[0].message.content)