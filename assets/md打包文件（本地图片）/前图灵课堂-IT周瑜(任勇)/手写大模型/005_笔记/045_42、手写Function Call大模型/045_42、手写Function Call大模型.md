# 42、手写Function Call大模型

# 手写Function Call大模型

作者：IT周瑜

微信ID：it_zhouyu

所谓Function Call大模型，就是大模型知道什么问题要调用工具以及传什么参数，什么问题不需要调用工具而是直接回答。

```python
# !pip install langchain
# !pip install langchain_deepseek
```

```python
import os
from typing import Annotated

from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek


@tool
def get_weather(city: Annotated[str, "城市名称"]) -> str:
    """获取指定城市的天气"""
    if city == "上海":
        return "阴天"
    if city == "北京":
        return "多云"
    return "下雨"


print(get_weather.name)
print(get_weather.description)
print(get_weather.args)
```

```plaintext
get_weather
获取指定城市的天气
{'city': {'description': '城市名称', 'title': 'City', 'type': 'string'}}
```

```python
os.environ["DEEPSEEK_API_KEY"] = "sk-a6a78e54f458437d9d315bf50fd3f663"

model = ChatDeepSeek(model="deepseek-chat")

tools = [get_weather]
model_with_tools = model.bind_tools(tools)

query = "上海什么天气"
response = model_with_tools.invoke(query)
# response返回的并不是最终的输出，而是一个Tool调用结果
print(response)
```

```plaintext
content='我来帮您查询上海的天气情况。' additional_kwargs={'tool_calls': [{'id': 'call_00_e851sSgrUX2ca4cuepMPi5vw', 'function': {'arguments': '{"city": "\\u4e0a\\u6d77"}', 'name': 'get_weather'}, 'type': 'function', 'index': 0}], 'refusal': None} response_metadata={'token_usage': {'completion_tokens': 30, 'prompt_tokens': 155, 'total_tokens': 185, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 128}, 'prompt_cache_hit_tokens': 128, 'prompt_cache_miss_tokens': 27}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_f253fc19d1_prod0820_fp8_kvcache', 'id': '1afebb68-ad34-4f6f-a38b-4a78f5348e39', 'service_tier': None, 'finish_reason': 'tool_calls', 'logprobs': None} id='run--a972e461-a79d-4b08-9488-d94e9c4c4372-0' tool_calls=[{'name': 'get_weather', 'args': {'city': '上海'}, 'id': 'call_00_e851sSgrUX2ca4cuepMPi5vw', 'type': 'tool_call'}] usage_metadata={'input_tokens': 155, 'output_tokens': 30, 'total_tokens': 185, 'input_token_details': {'cache_read': 128}, 'output_token_details': {}}
```

```python
tool_call = response.tool_calls[0]

# 执行工具
tools_map = {tool.name: tool for tool in tools}
result = tools_map[tool_call["name"]].invoke(tool_call["args"])
print(result)
```

```plaintext
阴天
```

```python
tools = [
    {
        "name": "get_weather",
        "description": "用于获取指定城市的天气情况",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名，例如：北京、上海"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_online",
        "description": "用于进行互联网实时搜索",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "需要搜索的关键词或问题"
                }
            },
            "required": ["query"]
        }
    }
]
```

```python
zhouyu_chat_template = """<|zhouyu_start|>system
{tools}<|zhouyu_end|>
<|zhouyu_start|>user
{question}<|zhouyu_end|>
<|zhouyu_start|>assistant
{answer}
<|zhouyu_end|>"""
```

```python
data = [
    {
        "tools": tools,
        "question": "我想知道上海什么天气？",
        "answer": """<tool_code>{"name": "get_weather","arguments": {"city": "上海"}}</tool_code>"""
    },
    {
        "tools": tools,
        "question": "什么是Transformer",
        "answer": """<tool_code>{"name": "search_online","arguments": {"query": "什么是Transformer"}}</tool_code>"""
    },
    {
        "tools": tools,
        "question": "你今天心情怎么样？",
        "answer": "心情很美丽"
    },
    {
        "tools": tools,
        "question": "帮我给it_zhouyu@qq.com发一封邮件，告诉他模型训练好了",
        "answer": "对不起，我没有发送邮件的功能，无法完成您的请求。"
    }
]
```

```python
test = zhouyu_chat_template.format(tools=data[0]["tools"], question=data[0]["question"], answer=data[0]["answer"])
print(test)
```

```plaintext
<|zhouyu_start|>system
[{'name': 'get_weather', 'description': '用于获取指定城市的天气情况', 'parameters': {'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名，例如：北京、上海'}}, 'required': ['city']}}, {'name': 'search_online', 'description': '用于进行互联网实时搜索', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': '需要搜索的关键词或问题'}}, 'required': ['query']}}]<|zhouyu_end|>
<|zhouyu_start|>user
我想知道上海什么天气？<|zhouyu_end|>
<|zhouyu_start|>assistant
<tool_code>{"name": "get_weather","arguments": {"city": "上海"}}</tool_code>
<|zhouyu_end|>
```

```python
from modelscope import AutoTokenizer, AutoModelForCausalLM

model_name = "openai-community/gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.add_special_tokens({'bos_token': '<|zhouyu_start|>'})
tokenizer.add_special_tokens({'eos_token': '<|zhouyu_end|>'})
tokenizer.add_special_tokens({'pad_token': '<|endoftext|>'})

model.resize_token_embeddings(len(tokenizer))
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2





Embedding(50259, 768)
```

```python
from torch.utils.data import Dataset


# 微信id：it_zhouyu
class ZhouyuDataset(Dataset):
    def __init__(self, data, max_length=512):
        self.encodings = []
        for qa in data:
            text = zhouyu_chat_template.format(tools=qa["tools"], question=qa["question"], answer=qa["answer"])
            encoded = tokenizer(
                text,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            input_ids = encoded['input_ids'].squeeze()
            self.encodings.append(input_ids)

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return self.encodings[idx]


dataset = ZhouyuDataset(data)
```

```python
dataset[0]
```

```plaintext
tensor([50257, 10057,   198,    58,    90,     6,  3672, 10354,   705,  1136,
           62, 23563,  3256,   705, 11213, 10354,   705, 18796,   101, 12859,
          236,   164,   236,   115, 20998,   244,   162,   234,   229, 22522,
          248,   161,   253,   236, 30585,   224, 21410, 25465, 36365,   242,
        46349,   227, 37863,   113,  3256,   705, 17143,  7307, 10354,  1391,
            6,  4906, 10354,   705, 15252,  3256,   705, 48310, 10354,  1391,
            6, 19205, 10354,  1391,     6,  4906, 10354,   705,  8841,  3256,
          705, 11213, 10354,   705,   161,   253,   236, 30585,   224, 28938,
          235,   171,   120,   234,   160,   122,   233, 36685,   224,   171,
          120,   248, 44293,   245, 12859,   105, 23513, 41468, 38184,   115,
            6,    92,  5512,   705, 35827, 10354, 37250, 19205, 20520,    92,
         5512,  1391,     6,  3672, 10354,   705, 12947,    62, 25119,  3256,
          705, 11213, 10354,   705, 18796,   101, 12859,   236, 32573,   249,
        26193,   234, 12859,   240,   164,   223,   242,   163,   121,   239,
        22522,   252, 33768, 35050,   238,   250,   163,   112,    95,  3256,
          705, 17143,  7307, 10354,  1391,     6,  4906, 10354,   705, 15252,
         3256,   705, 48310, 10354,  1391,     6, 22766, 10354,  1391,     6,
         4906, 10354,   705,  8841,  3256,   705, 11213, 10354,   705,   165,
          250,   222, 17358,   223,   162,   238,   250,   163,   112,    95,
        21410, 17739,   111,   165,   242,   106, 46237,   235, 22755,   244,
        29785,   106,   165,    95,   246,     6,    92,  5512,   705, 35827,
        10354, 37250, 22766, 20520, 11709,    60, 50258,   198, 50257,  7220,
          198, 22755,   239, 46349,   111,   163,   253,    98, 34402,   241,
        41468, 38184,   115, 20015,   222, 20046,   230, 25465, 36365,   242,
          171,   120,   253, 50258,   198, 50257,   562, 10167,   198,    27,
        25981,    62,  8189,    29,  4895,  3672,  1298,   366,  1136,    62,
        23563,  2430,   853,  2886,  1298, 19779, 19205,  1298,   366, 41468,
        38184,   115,     1, 11709,  3556, 25981,    62,  8189,    29,   198,
        50258, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256, 50256,
        50256, 50256])
```

```python

test = tokenizer.decode(dataset[0])
print(test)
```

```plaintext
<|zhouyu_start|>system
[{'name': 'get_weather', 'description': '用于获取指定城市的天气情况', 'parameters': {'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名，例如：北京、上海'}}, 'required': ['city']}}, {'name': 'search_online', 'description': '用于进行互联网实时搜索', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': '需要搜索的关键词或问题'}}, 'required': ['query']}}]<|zhouyu_end|>
<|zhouyu_start|>user
我想知道上海什么天气？<|zhouyu_end|>
<|zhouyu_start|>assistant
<tool_code>{"name": "get_weather","arguments": {"city": "上海"}}</tool_code>
<|zhouyu_end|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|>
```

```python
from transformers import DataCollatorForLanguageModeling

# 创建数据收集器
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # 使用CLM（因果语言模型）
)
```

```python
from transformers import Trainer, TrainingArguments

# 训练配置
training_args = TrainingArguments(
    output_dir="./zhouyu_functioncall_model",
    per_device_train_batch_size=1,
    num_train_epochs=100,
    # eval_strategy="epoch",
    # save_strategy="epoch",
    logging_steps=10
)

# 创建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    # eval_dataset=tokenized_datasets,
    data_collator=data_collator
)

# 开始训练
trainer.train()
trainer.save_model("./zhouyu_functioncall_model/model")
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/utils/data/dataloader.py:683: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, then device pinned memory won't be used.
  warnings.warn(warn_msg)




<div>

  <progress value='400' max='400' style='width:300px; height:20px; vertical-align: middle;'></progress>
  [400/400 02:09, Epoch 100/100]
</div>
<table border="1" class="dataframe">
```

Step Training Loss 10 2.544300 20 1.316700 30 0.750200 40 0.512500 50 0.406100 60 0.300200 70 0.238600 80 0.213100 90 0.174500 100 0.153100 110 0.103700 120 0.086300 130 0.083100 140 0.066700 150 0.050900 160 0.046000 170 0.071000 180 0.045500 190 0.037500 200 0.036000 210 0.033800 220 0.040400 230 0.032200 240 0.039200 250 0.027100 260 0.028100 270 0.028000 280 0.033700 290 0.027200 300 0.026700 310 0.030900 320 0.023200 330 0.033000 340 0.026600 350 0.023200 360 0.025100 370 0.020700 380 0.022900 390 0.024000 400 0.026600

```python
def get_weather(city: str) -> str:
    """用来获取天气"""
    return f"{city}天气是晴天"

chat_tools = [
    {
        "name": "get_weather",
        "description": "用来获取天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名，例如：北京、上海"
                }
            },
            "required": ["city"]
        }
    }
]
```

```python
import torch

chat_template = """<|zhouyu_start|>system
{tools}<|zhouyu_end|>
<|zhouyu_start|>user
{question}<|zhouyu_end|>
<|zhouyu_start|>assistant
"""

prompt = "我想知道上海什么天气？"
# prompt = "你今天心情怎么样？"

text = chat_template.format(tools=chat_tools, question=prompt)

device = torch.device("cuda" if torch.cuda.is_available() else "mps")
model_inputs = tokenizer([text], return_tensors="pt")
model_inputs = model_inputs.to(device)
generated_ids = model.generate(**model_inputs, max_new_tokens=200, pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|zhouyu_start|>system
[{'name': 'get_weather', 'description': '用来获取天气', 'parameters': {'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名，例如：北京、上海'}}, 'required': ['city']}}]<|zhouyu_end|>
<|zhouyu_start|>user
我想知道上海什么天气？<|zhouyu_end|>
<|zhouyu_start|>assistant
<tool_code>{"name": "get_weather","arguments": {"city": "上海"}}</tool_code>
<|zhouyu_end|>
```