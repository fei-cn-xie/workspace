# 38、LoRA微调Qwen3大模型实战

# LoRA

Low-Rank Adaptation, 低秩适配。

通过训练少量参数，来微调模型。

```python
from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-23 08:10:38,877 - modelscope - INFO - Target directory already exists, skipping creation.


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-23 08:10:43,899 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
prompt = "你是谁"
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False,  # 关闭了思考模式
)
print(text)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>
```

```python
model_inputs = tokenizer([text], return_tensors="pt")
generated_ids = model.generate(**model_inputs, max_new_tokens=32768)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是一个AI助手，我不会直接回答“你是谁”，但可以提供帮助。你可以告诉我你需要什么帮助，我会尽力为你服务！<|im_end|>
```

```python
data = [
    {"Q": "你是谁", "A": "我是大都督周瑜的AI助手"}
]
```

```python
# prompt = "问题:你是谁\n答案:我是大都督周瑜的AI助手"
```

<|im_start|>user
{你是谁}<|im_end|>
<|im_start|>assistant

{我是大都督周瑜的AI助手}<|im_end|>

```python
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
tokenizer.decode(151645), tokenizer.decode(151643)
```

```plaintext
('<|im_end|>', '<|endoftext|>')
```

```python
tokenizer.special_tokens_map
```

```plaintext
{'eos_token': '<|im_end|>',
 'pad_token': '<|endoftext|>',
 'additional_special_tokens': ['<|im_start|>',
  '<|im_end|>',
  '<|object_ref_start|>',
  '<|object_ref_end|>',
  '<|box_start|>',
  '<|box_end|>',
  '<|quad_start|>',
  '<|quad_end|>',
  '<|vision_start|>',
  '<|vision_end|>',
  '<|vision_pad|>',
  '<|image_pad|>',
  '<|video_pad|>']}
```

```python
!pip install peft
```

```plaintext
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
        - Avoid using `tokenizers` before the fork if possible
        - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)


Requirement already satisfied: peft in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (0.16.0)

Requirement already satisfied: numpy>=1.17 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (2.2.6)

Requirement already satisfied: packaging>=20.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (25.0)

Requirement already satisfied: psutil in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (7.0.0)

Requirement already satisfied: pyyaml in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (6.0.2)

Requirement already satisfied: torch>=1.13.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (2.7.1)

Requirement already satisfied: transformers in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (4.52.4)

Requirement already satisfied: tqdm in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (4.67.1)

Requirement already satisfied: accelerate>=0.21.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (1.9.0)

Requirement already satisfied: safetensors in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (0.5.3)

Requirement already satisfied: huggingface_hub>=0.25.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from peft) (0.33.0)

Requirement already satisfied: filelock in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from huggingface_hub>=0.25.0->peft) (3.18.0)

Requirement already satisfied: fsspec>=2023.5.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from huggingface_hub>=0.25.0->peft) (2024.9.0)

Requirement already satisfied: requests in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from huggingface_hub>=0.25.0->peft) (2.32.4)

Requirement already satisfied: typing-extensions>=3.7.4.3 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from huggingface_hub>=0.25.0->peft) (4.14.0)

Requirement already satisfied: hf-xet<2.0.0,>=1.1.2 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from huggingface_hub>=0.25.0->peft) (1.1.5)

Requirement already satisfied: sympy>=1.13.3 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from torch>=1.13.0->peft) (1.14.0)

Requirement already satisfied: networkx in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from torch>=1.13.0->peft) (3.4.2)

Requirement already satisfied: jinja2 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from torch>=1.13.0->peft) (3.1.6)

Requirement already satisfied: mpmath<1.4,>=1.1.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from sympy>=1.13.3->torch>=1.13.0->peft) (1.3.0)

Requirement already satisfied: MarkupSafe>=2.0 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from jinja2->torch>=1.13.0->peft) (3.0.2)

Requirement already satisfied: charset_normalizer<4,>=2 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from requests->huggingface_hub>=0.25.0->peft) (3.4.2)

Requirement already satisfied: idna<4,>=2.5 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from requests->huggingface_hub>=0.25.0->peft) (3.10)

Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from requests->huggingface_hub>=0.25.0->peft) (2.4.0)

Requirement already satisfied: certifi>=2017.4.17 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from requests->huggingface_hub>=0.25.0->peft) (2025.4.26)

Requirement already satisfied: regex!=2019.12.17 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from transformers->peft) (2024.11.6)

Requirement already satisfied: tokenizers<0.22,>=0.21 in /Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages (from transformers->peft) (0.21.2)
```

```python
print(model)
```

```plaintext
Qwen3ForCausalLM(
  (model): Qwen3Model(
    (embed_tokens): Embedding(151936, 1024)
    (layers): ModuleList(
      (0-27): 28 x Qwen3DecoderLayer(
        (self_attn): Qwen3Attention(
          (q_proj): Linear(in_features=1024, out_features=2048, bias=False)
          (k_proj): Linear(in_features=1024, out_features=1024, bias=False)
          (v_proj): Linear(in_features=1024, out_features=1024, bias=False)
          (o_proj): Linear(in_features=2048, out_features=1024, bias=False)
          (q_norm): Qwen3RMSNorm((128,), eps=1e-06)
          (k_norm): Qwen3RMSNorm((128,), eps=1e-06)
        )
        (mlp): Qwen3MLP(
          (gate_proj): Linear(in_features=1024, out_features=3072, bias=False)
          (up_proj): Linear(in_features=1024, out_features=3072, bias=False)
          (down_proj): Linear(in_features=3072, out_features=1024, bias=False)
          (act_fn): SiLU()
        )
        (input_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
        (post_attention_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
      )
    )
    (norm): Qwen3RMSNorm((1024,), eps=1e-06)
    (rotary_emb): Qwen3RotaryEmbedding()
  )
  (lm_head): Linear(in_features=1024, out_features=151936, bias=False)
)
```

```python
print(f'参数量：{sum(p.numel() for p in model.parameters())}')
```

```plaintext
参数量：596049920
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
trainable params: 401,408 || all params: 596,451,328 || trainable%: 0.0673
```

```python
596049920+401408
```

```plaintext
596451328
```

```python
print(f'参数量：{sum(p.numel() for p in model.parameters())}')
```

```plaintext
参数量：596451328
```

```python
print(model)
```

```plaintext
Qwen3ForCausalLM(
  (model): Qwen3Model(
    (embed_tokens): Embedding(151936, 1024)
    (layers): ModuleList(
      (0-27): 28 x Qwen3DecoderLayer(
        (self_attn): Qwen3Attention(
          (q_proj): lora.Linear(
            (base_layer): Linear(in_features=1024, out_features=2048, bias=False)
            (lora_dropout): ModuleDict(
              (default): Identity()
            )
            (lora_A): ModuleDict(
              (default): Linear(in_features=1024, out_features=2, bias=False)
            )
            (lora_B): ModuleDict(
              (default): Linear(in_features=2, out_features=2048, bias=False)
            )
            (lora_embedding_A): ParameterDict()
            (lora_embedding_B): ParameterDict()
            (lora_magnitude_vector): ModuleDict()
          )
          (k_proj): lora.Linear(
            (base_layer): Linear(in_features=1024, out_features=1024, bias=False)
            (lora_dropout): ModuleDict(
              (default): Identity()
            )
            (lora_A): ModuleDict(
              (default): Linear(in_features=1024, out_features=2, bias=False)
            )
            (lora_B): ModuleDict(
              (default): Linear(in_features=2, out_features=1024, bias=False)
            )
            (lora_embedding_A): ParameterDict()
            (lora_embedding_B): ParameterDict()
            (lora_magnitude_vector): ModuleDict()
          )
          (v_proj): lora.Linear(
            (base_layer): Linear(in_features=1024, out_features=1024, bias=False)
            (lora_dropout): ModuleDict(
              (default): Identity()
            )
            (lora_A): ModuleDict(
              (default): Linear(in_features=1024, out_features=2, bias=False)
            )
            (lora_B): ModuleDict(
              (default): Linear(in_features=2, out_features=1024, bias=False)
            )
            (lora_embedding_A): ParameterDict()
            (lora_embedding_B): ParameterDict()
            (lora_magnitude_vector): ModuleDict()
          )
          (o_proj): Linear(in_features=2048, out_features=1024, bias=False)
          (q_norm): Qwen3RMSNorm((128,), eps=1e-06)
          (k_norm): Qwen3RMSNorm((128,), eps=1e-06)
        )
        (mlp): Qwen3MLP(
          (gate_proj): Linear(in_features=1024, out_features=3072, bias=False)
          (up_proj): Linear(in_features=1024, out_features=3072, bias=False)
          (down_proj): Linear(in_features=3072, out_features=1024, bias=False)
          (act_fn): SiLU()
        )
        (input_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
        (post_attention_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
      )
    )
    (norm): Qwen3RMSNorm((1024,), eps=1e-06)
    (rotary_emb): Qwen3RotaryEmbedding()
  )
  (lm_head): Linear(in_features=1024, out_features=151936, bias=False)
)
```

```python

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
Epoch 1, Loss: 8.3108
Epoch 11, Loss: 0.4896
Epoch 21, Loss: 0.1294
Epoch 31, Loss: 0.1155
Epoch 41, Loss: 0.1101
```

```python
model_name = "Qwen/Qwen3-0.6B"
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
generated_ids = lora_model.generate(**model_inputs, max_new_tokens=32768)
# generated_ids = base_model.generate(**model_inputs, max_new_tokens=32768)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-17 19:13:24,517 - modelscope - INFO - Target directory already exists, skipping creation.


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
lora_model.save_pretrained("./Zhouyu-Qwen3-0.6B")
```

```python
from peft import PeftModel

from modelscope import AutoModelForCausalLM
from modelscope import AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = PeftModel.from_pretrained(model, "./Zhouyu-Qwen3-0.6B")
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-17 19:15:28,614 - modelscope - INFO - Target directory already exists, skipping creation.


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-17 19:15:34,563 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
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
generated_ids = model.generate(**model_inputs, max_new_tokens=32768)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是你的虚拟助手，我不会直接回答问题，我将根据你的问题提供帮助。<|im_end|>
```