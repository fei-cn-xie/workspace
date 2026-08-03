# 46、手写DeepSeek之模型黑盒蒸馏实战

## 模型蒸馏

所谓模型蒸馏，就是让一个Student Model学习Teacher Model的输出，通常Student Model是一个小模型，Teacher Model是一个大型模型，Teacher Model的训练数据集通常比Student Model的数据集大很多。

而所谓Teacher Model的输出分两种，根据输出可以分为两种蒸馏方式，一种是黑盒蒸馏，或者叫硬蒸馏，原理就是向Teacher Model提问，得到Teacher Model的答案，然后将问题和答案组织为训练数据，用来微调Student Model，这样Student Model就可以学习到Teacher Model的输出了。

另外一种是白盒蒸馏，后者叫软蒸馏，还是向Teacher Model提问，在底层，Teacher Model会输出每个Token的概率分布，直接让Student Model来学习这个概率分布，达到向Teacher Model学习的效果。

```python
from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

model_name = "Qwen/Qwen3-1.7B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-02 21:36:45,056 - modelscope - INFO - Target directory already exists, skipping creation.



Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]


Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-02 21:36:47,512 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
data = [
    {"Q": "你是谁", "A": "我是大都督周瑜的AI助手"}
]

from torch.utils.data import Dataset, DataLoader

lora_prompt_template = """
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
<think>

</think>
{answer}
<|im_end|>"""


class ZhouyuDataset(Dataset):
    def __init__(self, data, max_length=128):
        self.encodings = []
        for qa in data:
            text = lora_prompt_template.format(question=qa["Q"], answer=qa["A"])
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
data_loader = DataLoader(dataset, batch_size=1, shuffle=True)
for batch in data_loader:
    print(batch)
    break
```

```plaintext
tensor([[   198, 151644,    872,    198, 105043, 100165, 151645,    198, 151644,
          77091,    198, 151667,    271, 151668,    198, 104198,  26288,  71268,
          99625,  40542, 103487,   9370,  15469, 110498,    198, 151645, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643, 151643,
         151643, 151643]])
```

```python
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=2,
    target_modules=["q_proj", "k_proj", "v_proj"]
)

# 应用LoRA
lora_model = get_peft_model(model, lora_config)
lora_model.print_trainable_parameters()  # 查看可训练参数
```

```plaintext
trainable params: 573,440 || all params: 1,721,148,416 || trainable%: 0.0333
```

```python
import torch

optimizer = torch.optim.Adam(lora_model.parameters(), lr=0.001)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
lora_model.to(device)

EPOCHS = 50

for epoch in range(EPOCHS):

    for input_ids in data_loader:
        input_ids = input_ids.to(device)

        outputs = lora_model(
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
Epoch 1, Loss: 13.7732
Epoch 11, Loss: 0.6814
Epoch 21, Loss: 0.2855
Epoch 31, Loss: 0.1365
Epoch 41, Loss: 0.1266
```

```python
model_name = "Qwen/Qwen3-1.7B"
base_model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "你是谁"
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False
)
model_inputs = tokenizer([text], return_tensors="pt")
model_inputs = model_inputs.to(device)
generated_ids = lora_model.generate(**model_inputs, max_new_tokens=256)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-02 21:37:49,946 - modelscope - INFO - Target directory already exists, skipping creation.



Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]


<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是大都督周瑜的AI助手
<|im_end|>
```

```python
# 保存LoRA学到的参数
lora_model.save_pretrained("./Zhouyu-Qwen3-1.7B")
```

## 模型蒸馏-黑盒蒸馏

```python
from peft import PeftModel

from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

teacher_model_name = "Qwen/Qwen3-1.7B"
teacher_base_model = AutoModelForCausalLM.from_pretrained(teacher_model_name)
teacher_tokenizer = AutoTokenizer.from_pretrained(teacher_model_name)
teacher_model = PeftModel.from_pretrained(teacher_base_model, "./Zhouyu-Qwen3-1.7B")
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-02 22:06:30,891 - modelscope - INFO - Target directory already exists, skipping creation.



Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]


Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-02 22:06:32,993 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
prompt = "你是谁"
messages = [
    {"role": "user", "content": prompt}
]
text = teacher_tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False
)
model_inputs = teacher_tokenizer([text], return_tensors="pt")
generated_ids = teacher_model.generate(**model_inputs, max_new_tokens=256)
content = teacher_tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是大都督周瑜的AI助手
<|im_end|>
```

```python
# Student Model
from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

student_model_name = "Qwen/Qwen3-0.6B"
student_model = AutoModelForCausalLM.from_pretrained(student_model_name)
student_tokenizer = AutoTokenizer.from_pretrained(student_model_name)
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-08-02 22:06:47,125 - modelscope - INFO - Target directory already exists, skipping creation.


Downloading Model from https://www.modelscope.cn to directory: /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-08-02 22:06:48,677 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
# 蒸馏数据
distillation_data = ["你是谁"]

from torch.utils.data import Dataset, DataLoader

chat_prompt_template = """
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
<think>

</think>
"""


class ZhouyuDistillationDataset(Dataset):
    def __init__(self, data, max_length=128):
        self.encodings = []
        for question in data:
            text = chat_prompt_template.format(question=question)
            print(text)
            encoded = teacher_tokenizer(
                [text],
                return_tensors='pt'
            )
            input_ids = encoded['input_ids'].squeeze()
            self.encodings.append(input_ids)

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return self.encodings[idx]


distillation_dataset = ZhouyuDistillationDataset(distillation_data)
distillation_dataloader = DataLoader(distillation_dataset, batch_size=1, shuffle=True)
for batch in distillation_dataloader:
    print(batch)
    break
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

tensor([[   198, 151644,    872,    198, 105043, 100165, 151645,    198, 151644,
          77091,    198, 151667,    271, 151668,    198]])
```

```python
import torch

optimizer = torch.optim.Adam(student_model.parameters(), lr=5e-5)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
teacher_model.to(device)
student_model.to(device)

EPOCHS = 100

for epoch in range(EPOCHS):

    for input_ids in distillation_dataloader:
        input_ids = input_ids.to(device)

        # 得到教师模型的输出
        with torch.no_grad():
            teacher_outputs = teacher_model.generate(input_ids, max_new_tokens=256)
            # content = teacher_tokenizer.decode(teacher_outputs[0])
            # print(content)

        outputs = student_model(
            teacher_outputs, labels=teacher_outputs
        )

        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')
```

```plaintext
Epoch 1, Loss: 2.4878
Epoch 11, Loss: 11.4409
Epoch 21, Loss: 7.7254
Epoch 31, Loss: 3.1194
Epoch 41, Loss: 2.4446
Epoch 51, Loss: 1.9051
Epoch 61, Loss: 1.4154
Epoch 71, Loss: 0.7498
Epoch 81, Loss: 0.8846
Epoch 91, Loss: 0.2167
```

```python

prompt = "你是谁"
messages = [
    {"role": "user", "content": prompt}
]
text = student_tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False
)
model_inputs = student_tokenizer([text], return_tensors="pt")
model_inputs = model_inputs.to(device)
generated_ids = student_model.generate(**model_inputs, max_new_tokens=256)
content = student_tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是大都督周瑜的AI助手
<|im_end|>
```