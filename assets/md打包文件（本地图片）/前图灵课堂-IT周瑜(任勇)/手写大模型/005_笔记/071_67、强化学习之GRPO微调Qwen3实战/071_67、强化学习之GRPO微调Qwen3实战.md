# 67、强化学习之GRPO微调Qwen3实战

状态=问题
动作=输出下一token
奖励=人类定义奖励规则
轨迹=答案

## 大模型训练的三个阶段

1. 预训练：在海量、无标注的互联网文本数据上训练模型，使其掌握基本的语言规律（语法、句法）、事实知识（历史事件、科学概念）和一定的逻辑推理能力
2. SFT：Supervised Fine-Tuning，监督微调，在高质量的指令-应答对上训练模型，使其学会理解并遵循人类的指令，并以期望的格式（如对话、列表、分析报告）进行回应
3. RLHF：Reinforcement Learning from Human Feedback， 基于人类反馈的强化学习，目标是让模型的回答不仅“正确”，而且“优秀”，符合人类最细微的偏好

总结比喻：
预训练：像让一个孩子博览群书，学会识字、造句和了解世界百科。
SFT：像给孩子请一个家教，通过具体的例题和范文，教他如何写特定格式的作文（如书信、报告）。
RLHF：像把孩子的作文拿去参加作文比赛，由多位评委（人类反馈）评分，他从中学会什么样的作文更能打动人心，从而不断精进写作技巧。

## RLHF的流程

1. 输入提示词给SFT模型，得到n个输出
2. 让人类标注人员对n个输出按照质量从高到底进行排序
3. 用标注后的数据训练奖励模型，输入一句话得到一个奖励分数（基于SFT模型训练出来的）
4. 使用PPO或GRPO微调SFT模型，使得能够根据奖励模型来微调，提高生成高质量答案（人类觉得质量高）的概率

```python
# pip install transformers trl peft accelerate bitsandbytes hf_transfer
```

```python
import torch

print(torch.__version__)  # PyTorch 版本
print(torch.version.cuda)  # CUDA 版本
print(torch.cuda.is_available())  # 检查 CUDA 是否可用
```

```python
# !pip install --upgrade torch torchvision torchaudio
```

```python
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
```

```python
from datasets import Dataset

# 准备 5 条简单的教学数据
data = {
    "prompt": [
                  "问题：15 + 27 等于多少？",
                  "问题：如果我有 3 个苹果，又买了 5 个，现在有几个？",
                  "问题：99 - 18 等于多少？",
                  "问题：2 乘以 6 等于多少？",
                  "问题：120 除以 4 是多少？"
              ],
    "answer": ["42", "8", "81", "12", "30"]
}
dataset = Dataset.from_dict(data)
```

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import GRPOTrainer, GRPOConfig
from peft import LoraConfig, get_peft_model

MODEL_ID = "Qwen/Qwen3-0.6B"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
```

```python
# 定义奖励函数
def reward_func(completions, answer, **kwargs):
    """奖励模型给出正确答案"""
    rewards = []
    for content, ans in zip(completions, answer):
        # 如果回答中包含了正确数字，给 1.5 分
        if ans in content:
            rewards.append(1.5)
        else:
            rewards.append(0.0)
    return rewards


def run_inference(model, tokenizer, prompt):
    input_text = f"User: {prompt}\nAssistant: "
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=128, do_sample=True)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

```python
# 展示微调前的效果
test_prompt = "25 + 38 等于多少？"
run_inference(model, tokenizer, test_prompt)
```

```python
# 训练
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj"],
    task_type="CAUSAL_LM"
)

# 问题
training_args = GRPOConfig(
    output_dir="./qwen-grpo-demo",
    learning_rate=1e-5,
    per_device_train_batch_size=4,
    num_generations=4,  # 每一行数据生成 4 个回答进行组内对比
    max_prompt_length=64,
    max_completion_length=256,
    logging_steps=1,
    num_train_epochs=1,
    save_strategy="no"
)

trainer = GRPOTrainer(
    model=model,
    reward_funcs=[reward_func],
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config,
)
trainer.train()
```

```python
# 展示微调后的效果
test_prompt = "25 + 38 等于多少？"
run_inference(model, tokenizer, test_prompt)
```