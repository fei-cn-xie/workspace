# 41、HuggingFace微调大模型实战

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


2025-07-18 11:00:11,134 - modelscope - INFO - Target directory already exists, skipping creation.


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-07-18 11:00:17,342 - modelscope - INFO - Target directory already exists, skipping creation.
```

```python
data = [
    {"Q": "你是谁", "A": "我是大都督周瑜的AI助手"}
]
```

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
# !pip install peft
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
from transformers import Trainer, TrainingArguments

# 训练配置
training_args = TrainingArguments(
    output_dir="./huggingface_lora_qwen3",
    per_device_train_batch_size=4,
    num_train_epochs=150,
    logging_steps=10
)

# 创建Trainer
trainer = Trainer(
    model=lora_model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)

# 开始训练
trainer.train()
```

```plaintext
No label_names provided for model class `PeftModelForCausalLM`. Since `PeftModel` hides base models input arguments, if label_names is not given, label_names can't be set automatically within `Trainer`. Note that empty label_names list will be used instead.
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/utils/data/dataloader.py:683: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, then device pinned memory won't be used.
  warnings.warn(warn_msg)




<div>

  <progress value='150' max='150' style='width:300px; height:20px; vertical-align: middle;'></progress>
  [150/150 00:42, Epoch 150/150]
</div>
<table border="1" class="dataframe">
```

Step Training Loss 10 6.888900 20 5.536500 30 4.274200 40 3.328500 50 2.496600 60 1.797400 70 1.219500 80 0.907000 90 0.727400 100 0.643000 110 0.610300 120 0.596700 130 0.589600 140 0.585600 150 0.583700

```plaintext
TrainOutput(global_step=150, training_loss=2.0523267300923664, metrics={'train_runtime': 43.6353, 'train_samples_per_second': 3.438, 'train_steps_per_second': 3.438, 'total_flos': 50788093132800.0, 'train_loss': 2.0523267300923664, 'epoch': 150.0})
```

```python
import torch

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

device = torch.device("cuda" if torch.cuda.is_available() else "mps")
model_inputs = tokenizer([text], return_tensors="pt")
model_inputs = model_inputs.to(device)
generated_ids = lora_model.generate(**model_inputs, max_new_tokens=32768)
content = tokenizer.decode(generated_ids[0])
print(content)
```

```plaintext
<|im_start|>user
你是谁<|im_end|>
<|im_start|>assistant
<think>

</think>

我是大都督周瑜的AI助手<|im_end|>
```