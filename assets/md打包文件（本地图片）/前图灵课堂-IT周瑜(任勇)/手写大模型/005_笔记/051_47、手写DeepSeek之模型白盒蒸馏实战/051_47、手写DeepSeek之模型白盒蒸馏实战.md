# 47、手写DeepSeek之模型白盒蒸馏实战

## 模型蒸馏-白盒蒸馏

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
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-03 07:00:16,449 - modelscope - INFO - Target directory already exists, skipping creation.
Loading checkpoint shards: 100%|██████████| 2/2 [00:09<00:00,  4.56s/it]


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-1.7B


2025-08-03 07:00:27,082 - modelscope - INFO - Target directory already exists, skipping creation.
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
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-08-03 07:00:50,788 - modelscope - INFO - Target directory already exists, skipping creation.


Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B


2025-08-03 07:00:56,730 - modelscope - INFO - Target directory already exists, skipping creation.
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

EPOCHS = 50

for epoch in range(EPOCHS):

    for input_ids in distillation_dataloader:
        input_ids = input_ids.to(device)

        # 得到下一个词的概率分布
        # with torch.no_grad():
        #     teacher_outputs = []
        #     current_inputs = input_ids.clone()
        #
        #     # 自回归生成
        #     for _ in range(input_ids.size(1)):
        #         outputs = teacher_model(current_inputs)
        #         teacher_logits = outputs.logits[:, -1, :]
        #         teacher_outputs.append(teacher_logits)
        #
        #         # 取概率最大的token继续生成
        #         next_tokens = torch.argmax(teacher_logits, dim=-1)
        #         current_inputs = torch.cat([current_inputs, next_tokens.unsqueeze(-1)], dim=-1)
        #
        #     teacher_logits = torch.stack(teacher_outputs, dim=1)  # [batch, seq_len, vocab]
        #
        # student_outputs = []
        # current_inputs = input_ids.clone()
        # for i in range(input_ids.size(1)):
        #     outputs = student_model(current_inputs)
        #     student_logits = outputs.logits[:, -1, :]
        #     student_outputs.append(student_logits)
        #
        #     # 取概率最大的token继续生成
        #     next_tokens = torch.argmax(student_logits, dim=-1)
        #     current_inputs = torch.cat([current_inputs, next_tokens.unsqueeze(-1)], dim=-1)
        #
        # student_logits = torch.stack(student_outputs, dim=1)

        with torch.no_grad():
            teacher_outputs = teacher_model(input_ids, labels=input_ids)
            teacher_logits = teacher_outputs.logits

        student_outputs = student_model(
            input_ids, labels=input_ids
        )
        student_logits = student_outputs.logits

        # 软目标损失
        soft_loss = torch.nn.functional.kl_div(
            torch.log_softmax(student_logits, dim=-1),
            torch.softmax(teacher_logits, dim=-1),
            reduction='batchmean'
        )


        optimizer.zero_grad()
        soft_loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch {epoch + 1}, Loss: {soft_loss:.4f}')
```

```plaintext
CausalLMOutputWithPast(loss=tensor(1.1071), logits=tensor([[[ 4.1185,  5.5874,  7.1719,  ...,  0.4592,  0.4592,  0.4592],
         [ 2.2171,  3.7658,  7.7227,  ..., -0.1603, -0.1604, -0.1604],
         [ 2.7057,  1.1595,  4.4529,  ...,  0.3835,  0.3835,  0.3835],
         ...,
         [-8.8077, -3.2438, -4.8060,  ..., -0.8007, -0.8007, -0.8007],
         [ 2.5121,  5.8145,  6.2906,  ..., -0.6621, -0.6621, -0.6620],
         [-1.7819,  4.2719, -0.8884,  ..., -0.3974, -0.3974, -0.3976]]]), past_key_values=<transformers.cache_utils.DynamicCache object at 0x3d79b8550>, hidden_states=None, attentions=None)



---------------------------------------------------------------------------

KeyboardInterrupt                         Traceback (most recent call last)

Cell In[8], line 45
     42 combined_loss = SOFT_LOSS_WEIGHT * soft_loss + HARD_LOSS_WEIGHT * hard_loss
     44 optimizer.zero_grad()
---> 45 combined_loss.backward()
     46 optimizer.step()
     48 if epoch % 10 == 0:


File ~/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/_tensor.py:648, in Tensor.backward(self, gradient, retain_graph, create_graph, inputs)
    638 if has_torch_function_unary(self):
    639     return handle_torch_function(
    640         Tensor.backward,
    641         (self,),
   (...)
    646         inputs=inputs,
    647     )
--> 648 torch.autograd.backward(
    649     self, gradient, retain_graph, create_graph, inputs=inputs
    650 )


File ~/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/autograd/__init__.py:307, in backward(tensors, grad_tensors, retain_graph, create_graph, grad_variables, inputs)
    243 def backward(
    244     tensors: _TensorOrTensorsOrGradEdge,
    245     grad_tensors: Optional[_TensorOrTensors] = None,
   (...)
    249     inputs: Optional[_TensorOrTensorsOrGradEdge] = None,
    250 ) -> None:
    251     r"""Compute the sum of gradients of given tensors with respect to graph leaves.
    252 
    253     The graph is differentiated using the chain rule. If any of ``tensors``
   (...)
    305             were used to compute the :attr:`tensors`.
    306     """
--> 307     if torch._C._are_functorch_transforms_active():
    308         raise RuntimeError(
    309             "backward() called inside a functorch transform. This is not "
    310             "supported, please use functorch.grad or functorch.vjp instead "
    311             "or call backward() outside of functorch transforms."
    312         )
    314     if grad_variables is not None:


KeyboardInterrupt: 
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
    enable_thinking=False,
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