# 37、全量微调一个问答ChatBot

```python
from modelscope.msdatasets import MsDataset

dataset = MsDataset.load('train.jsonl')
data = dataset.to_hf_dataset().select(range(10))
data[:10]
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
2025-07-17 08:44:07,475 - modelscope - WARNING - Use trust_remote_code=True. Will invoke codes from train.jsonl. Please make sure that you can trust the external codes.
2025-07-17 08:44:07,476 - modelscope - WARNING - Use trust_remote_code=True. Will invoke codes from json. Please make sure that you can trust the external codes.





{'question': ['你好，最近怎么样？',
  '今天天气如何？',
  '你喜欢旅行吗？',
  '你最喜欢的食物是什么？',
  '你有什么兴趣爱好？',
  '你最喜欢的电影是什么？',
  '你喜欢听音乐吗？',
  '你最喜欢的季节是哪个？',
  '你有什么宠物吗？',
  '你有宠物吗？'],
 'answer': ['你好！我最近还不错，谢谢。',
  '今天的天气很晴朗。',
  '是的，我非常喜欢旅行。',
  '我最喜欢的食物是寿司。',
  '我喜欢阅读和运动。',
  '我最喜欢的电影是《肖申克的救赎》。',
  '是的，我喜欢听流行音乐。',
  '我最喜欢的季节是夏天。',
  '是的，我有一只猫。',
  '是的，我有一只猫。'],
 'history': [None, None, None, None, None, None, None, None, None, None]}
```

```python
from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

model_name = "openai-community/gpt2"
gpt_model = AutoModelForCausalLM.from_pretrained(model_name)
gpt_tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
gpt_tokenizer.pad_token = gpt_tokenizer.eos_token
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2
```

```python
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

# 大都督周瑜（我的微信: it_zhouyu）

prompt = "问题:{}\n答案:"
# prompt = "{}"

class ChatBotDataset(Dataset):
    def __init__(self, data, max_length=128):
        self.data = data
        self.encodings = []
        for qa in data:  # 遍历文件的每一行
            # 将问题+答案拼接为单序列
            text = prompt.format(qa['question']) + qa['answer'] + gpt_tokenizer.eos_token
            # text = qa['question'] + qa['answer'] + gpt_tokenizer.eos_token
            print(text)
            encoded = gpt_tokenizer(
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

chat_dataset = ChatBotDataset(data)
data_loader = DataLoader(chat_dataset, batch_size=8, shuffle=True)
for batch in data_loader:
    print(batch)
    break
```

```plaintext
问题:你好，最近怎么样？
答案:你好！我最近还不错，谢谢。<|endoftext|>
问题:今天天气如何？
答案:今天的天气很晴朗。<|endoftext|>
问题:你喜欢旅行吗？
答案:是的，我非常喜欢旅行。<|endoftext|>
问题:你最喜欢的食物是什么？
答案:我最喜欢的食物是寿司。<|endoftext|>
问题:你有什么兴趣爱好？
答案:我喜欢阅读和运动。<|endoftext|>
问题:你最喜欢的电影是什么？
答案:我最喜欢的电影是《肖申克的救赎》。<|endoftext|>
问题:你喜欢听音乐吗？
答案:是的，我喜欢听流行音乐。<|endoftext|>
问题:你最喜欢的季节是哪个？
答案:我最喜欢的季节是夏天。<|endoftext|>
问题:你有什么宠物吗？
答案:是的，我有一只猫。<|endoftext|>
问题:你有宠物吗？
答案:是的，我有一只猫。<|endoftext|>
tensor([[29785,   106,   165,  ..., 50256, 50256, 50256],
        [29785,   106,   165,  ..., 50256, 50256, 50256],
        [29785,   106,   165,  ..., 50256, 50256, 50256],
        ...,
        [29785,   106,   165,  ..., 50256, 50256, 50256],
        [29785,   106,   165,  ..., 50256, 50256, 50256],
        [29785,   106,   165,  ..., 50256, 50256, 50256]])
```

```python
import torch
import torch.nn as nn

optimizer = torch.optim.Adam(gpt_model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
gpt_model.to(device)

EPOCHS = 50

for epoch in range(EPOCHS):

    for input_ids in data_loader:
        input_ids = input_ids.to(device)

        outputs = gpt_model(
            input_ids, labels=input_ids
        )

        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')
```

```plaintext
`loss_type=None` was set in the config but it is unrecognised.Using the default loss: `ForCausalLMLoss`.


Epoch 1, Loss: 9.6288
Epoch 1, Loss: 3.3672
Epoch 11, Loss: 0.5160
Epoch 11, Loss: 0.6401
Epoch 21, Loss: 0.1413
Epoch 21, Loss: 0.1014
Epoch 31, Loss: 0.0427
Epoch 31, Loss: 0.0476
Epoch 41, Loss: 0.0275
Epoch 41, Loss: 0.0267
```

```python
print(f'参数量：{sum(p.numel() for p in gpt_model.parameters())}')
```

```plaintext
参数量：124439808
```

```python
def generate(sentence, max_length=500):
    input_ids = gpt_tokenizer.encode(sentence, return_tensors='pt')
    input_ids = input_ids.to(device)
    output = gpt_model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id = gpt_tokenizer.eos_token_id,
        # do_sample=True,
    )
    return gpt_tokenizer.decode(output[0], skip_special_tokens=True)

input = prompt.format("你喜欢听音乐吗")
# input = "今天天气如何"
print(generate(input)[len(input):])
```

```plaintext
是的，我非常喜欢旅行。
```

## 模型本地保存和加载

```python
gpt_model.save_pretrained("./zhouyu_gpt_model")
```

```python
zhouyu_gpt_model = AutoModelForCausalLM.from_pretrained("./zhouyu_gpt_model")
```

```python
def generate(sentence, model, max_length=500):
    input_ids = gpt_tokenizer.encode(sentence, return_tensors='pt')
    input_ids = input_ids.to(device)
    output = model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id = gpt_tokenizer.eos_token_id,
        # do_sample=True,
    )
    return gpt_tokenizer.decode(output[0], skip_special_tokens=True)

input = prompt.format("你喜欢听音乐吗")
# input = "今天天气如何"
print(generate(input, model=zhouyu_gpt_model)[len(input):])
```

```plaintext
是的，我非常喜欢旅行。
```