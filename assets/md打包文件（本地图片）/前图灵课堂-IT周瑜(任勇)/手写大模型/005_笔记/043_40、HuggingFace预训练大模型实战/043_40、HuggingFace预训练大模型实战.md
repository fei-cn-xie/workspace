# 40、HuggingFace预训练大模型实战

```python
from modelscope import AutoTokenizer, AutoModelForCausalLM

model_name = "openai-community/gpt2"
gpt_model = AutoModelForCausalLM.from_pretrained(model_name)
gpt_tokenizer = AutoTokenizer.from_pretrained(model_name)
# gpt_tokenizer.pad_token = gpt_tokenizer.eos_token
gpt_tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# gpt_tokenizer.add_special_tokens({'mask_token': '[MASK]'})
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2





1
```

```python
from modelscope.msdatasets import MsDataset

dataset = MsDataset.load('modelscope/chinese-poetry-collection', subset_name='default', split='train')
data = dataset.to_hf_dataset().select(range(1))
```

```plaintext
2025-07-18 10:55:35,454 - modelscope - WARNING - Use trust_remote_code=True. Will invoke codes from chinese-poetry-collection. Please make sure that you can trust the external codes.
2025-07-18 10:55:37,195 - modelscope - WARNING - Reusing dataset dataset_builder (/Users/dadudu/.cache/modelscope/hub/datasets/modelscope/chinese-poetry-collection/master/data_files)
2025-07-18 10:55:37,196 - modelscope - INFO - Generating dataset dataset_builder (/Users/dadudu/.cache/modelscope/hub/datasets/modelscope/chinese-poetry-collection/master/data_files)
2025-07-18 10:55:37,196 - modelscope - INFO - Reusing cached meta-data file: /Users/dadudu/.cache/modelscope/hub/datasets/modelscope/chinese-poetry-collection/master/data_files/7c9a7977d937face2055b6145eaf516f
```

```python
# 数据预处理
def tokenize_function(examples):
    # 拼接EOS标记并编码
    poems = [p + gpt_tokenizer.eos_token for p in examples["text1"]]
    return gpt_tokenizer(poems, max_length=128, padding="max_length", truncation=True)


tokenized_datasets = data.map(tokenize_function, batched=True, remove_columns=data.column_names)
```

```plaintext
Map: 100%|██████████| 1/1 [00:00<00:00, 76.52 examples/s]
```

```python
from transformers import DataCollatorForLanguageModeling

# 创建数据收集器
data_collator = DataCollatorForLanguageModeling(
    tokenizer=gpt_tokenizer,
    mlm=False  # 使用CLM（因果语言模型）
)
```

```python
data_collator([[1, 2, 3, 4], [1, 2]])
```

```plaintext
{'input_ids': tensor([[    1,     2,     3,     4],
         [    1,     2, 50257, 50257]]),
 'labels': tensor([[   1,    2,    3,    4],
         [   1,    2, -100, -100]])}
```

```python
from transformers import Trainer, TrainingArguments

# 训练配置
training_args = TrainingArguments(
    output_dir="./huggingface_gpt",
    per_device_train_batch_size=4,
    num_train_epochs=100,
    # eval_strategy="epoch",
    # save_strategy="epoch",
    logging_steps=10
)

# 创建Trainer
trainer = Trainer(
    model=gpt_model,
    args=training_args,
    train_dataset=tokenized_datasets,
    # eval_dataset=tokenized_datasets,
    data_collator=data_collator
)

# 开始训练
trainer.train()
trainer.save_model("./huggingface_gpt/model")
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/utils/data/dataloader.py:683: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, then device pinned memory won't be used.
  warnings.warn(warn_msg)
`loss_type=None` was set in the config but it is unrecognised.Using the default loss: `ForCausalLMLoss`.




<div>

  <progress value='100' max='100' style='width:300px; height:20px; vertical-align: middle;'></progress>
  [100/100 00:15, Epoch 100/100]
</div>
<table border="1" class="dataframe">
```

Step Training Loss 10 2.666500 20 0.653400 30 0.105700 40 0.064100 50 0.021700 60 0.063600 70 0.043900 80 0.070200 90 0.032700 100 0.056300

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "mps")


def generate(sentence, max_length=100):
    inputs = gpt_tokenizer.encode(sentence, return_tensors='pt')
    input_ids = inputs.to(device)
    output = gpt_model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id=gpt_tokenizer.pad_token_id,
        eos_token_id=gpt_tokenizer.eos_token_id,
        do_sample=True
    )
    return gpt_tokenizer.decode(output[0], skip_special_tokens=True)


print(generate("半生"))
```

```plaintext
半生长以客为家，罢直初来瀚海槎。始信人间行不尽，天涯更复有天涯。
```

```python
from transformers import pipeline

# 使用pipeline进行文本生成
text_generator = pipeline(
    task="text-generation",
    model="./huggingface_gpt/model",
    tokenizer=gpt_tokenizer
)

# 生成文本
results = text_generator(
    "半生",
    pad_token_id=gpt_tokenizer.pad_token_id,
    eos_token_id=gpt_tokenizer.eos_token_id,
    do_sample=True
)

# 输出结果
print(results[0]['generated_text'])
```

```plaintext
Device set to use mps:0


半生长以客为家，罢直初来瀚海槎。始信人间行不尽，天涯更复有天涯。
```