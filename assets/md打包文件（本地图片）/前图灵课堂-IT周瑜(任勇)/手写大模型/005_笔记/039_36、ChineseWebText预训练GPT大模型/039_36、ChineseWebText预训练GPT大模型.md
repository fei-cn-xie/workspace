# 36、ChineseWebText预训练GPT大模型

```python
from transformers import GPT2Config, GPT2LMHeadModel

config = GPT2Config(n_layer=2, n_head=2, n_embd=192)
# config = GPT2Config(n_layer=4, n_head=4, n_embd=768)
# config = GPT2Config()
gpt_model = GPT2LMHeadModel(config)
print(gpt_model)
```

```plaintext
GPT2LMHeadModel(
  (transformer): GPT2Model(
    (wte): Embedding(50257, 192)
    (wpe): Embedding(1024, 192)
    (drop): Dropout(p=0.1, inplace=False)
    (h): ModuleList(
      (0-1): 2 x GPT2Block(
        (ln_1): LayerNorm((192,), eps=1e-05, elementwise_affine=True)
        (attn): GPT2Attention(
          (c_attn): Conv1D(nf=576, nx=192)
          (c_proj): Conv1D(nf=192, nx=192)
          (attn_dropout): Dropout(p=0.1, inplace=False)
          (resid_dropout): Dropout(p=0.1, inplace=False)
        )
        (ln_2): LayerNorm((192,), eps=1e-05, elementwise_affine=True)
        (mlp): GPT2MLP(
          (c_fc): Conv1D(nf=768, nx=192)
          (c_proj): Conv1D(nf=192, nx=768)
          (act): NewGELUActivation()
          (dropout): Dropout(p=0.1, inplace=False)
        )
      )
    )
    (ln_f): LayerNorm((192,), eps=1e-05, elementwise_affine=True)
  )
  (lm_head): Linear(in_features=192, out_features=50257, bias=False)
)
```

```python
from modelscope import AutoTokenizer
gpt_tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/openai-community/gpt2
```

```python
import torch
import torch.nn as nn
from modelscope.msdatasets import MsDataset

# 读取chinese_web_text.jsonl文件
dataset = MsDataset.load('chinese_web_text.jsonl')

data = dataset.to_hf_dataset().select(range(1))

data[:1]
```

```plaintext
2025-07-16 15:26:55,087 - modelscope - WARNING - Use trust_remote_code=True. Will invoke codes from chinese_web_text.jsonl. Please make sure that you can trust the external codes.
2025-07-16 15:26:55,088 - modelscope - WARNING - Use trust_remote_code=True. Will invoke codes from json. Please make sure that you can trust the external codes.





{'text': [['PVC片材石塑地板、PVC卷材、PVC防静电地板、PVC锁扣地板、高架地板以及悬浮拼装运动地板和微晶石地板等。公司自成立伊始一直专注于地面材料领域的研究与开发，在不断引进国外先进的技术的同时，积极投入产品研发。公司旗下有“捷装”和“心牧”两大品牌，先后推出运动PVC地板、同质透心PVC地板、致密PVC地板、吸音PVC地板、装饰PVC地板、工业PVC地板、PVC防静电地板、防滑PVC地板等，同时代理金象产品橡胶地板，PVC弹性卷材地板、PVC同质透心卷材地板。\n公司产品获得“3C认证（中国强制产品认证）”、“欧盟CE认证”、"中国船级社CCS认证"、"铁道部科学研究院资质认证"、"ISO9000认证"、"国家质量检测CNAS"等特殊领域资格认证的高新技术企业。产品广泛应用于室内家庭、医院、学校、办公楼、工厂、公共场所、超市、商业、体育场馆等各种场所，同时出口到欧美、中东、俄罗斯、日韩等国家。随着市场的发展，公司不断努力，在专注于产品本身的同时运用现代化管理，致力于服务领域，以市场为导向，服务客户为核心的价值观，实现快速、稳定的发展。到目前为止公司营销服务网络已遍布全国，在全国多地均设有办事处或分公司。']],
 'info': [{'url': 'https://zh-cn.eturbonews.com/3005332/%E5%8A%A0%E6%8B%BF%E5%A4%A7%E6%B8%B8%E5%AE%A2%E6%96%B0%E8%BE%B9%E5%A2%83%E8%A7%84%E5%88%99-%E7%BE%8E%E5%9B%BD-10-%E4%B8%AA%E5%B7%9E%E5%B0%86%E5%BC%A0%E5%BC%80%E5%8F%8C%E8%87%82%E6%AC%A2%E8%BF%8E%E5%8A%A0%E6%8B%BF%E5%A4%A7%E4%BA%BA/',
   'title': '美国10个州将张开双臂欢迎加拿大人',
   'source_domain': 'zh-cn.eturbonews.com'}],
 'score': [[0.42278623290512307]]}
```

```python
gpt_tokenizer.encode("我今天很开心")
```

```plaintext
[22755, 239, 20015, 232, 25465, 36181, 230, 28156, 222, 33232, 225]
```

```python
from torch.utils.data import Dataset, DataLoader

class ZhouyuDataset(Dataset):
    def __init__(self, data, tokenizer, block_size=64):
        self.tokenizer = tokenizer
        self.block_size = block_size
        self.blocks = []

        for i in range(len(data)):
            text = data[i]['text'][0] + gpt_tokenizer.eos_token
            tokenized = tokenizer.encode(text)

            # 分割成长度为block_size的块
            for i in range(0, len(tokenized) - block_size + 1, block_size):
                self.blocks.append(tokenized[i:i + block_size])

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, idx):
        input_ids = self.blocks[idx]
        return torch.tensor(input_ids)


dataset = ZhouyuDataset(data, gpt_tokenizer)
data_loader = DataLoader(dataset, batch_size=2, shuffle=False)
for input_ids in data_loader:
    print(input_ids)
    break
```

```plaintext
tensor([[   47, 15922, 31965,   229, 30266,   238,   163,   253,   111,   161,
            94,   239, 28839,   108, 30266,   123, 23513,    47, 15922, 39355,
           115, 30266,   238, 23513,    47, 15922,   165,   246,   110,   165,
           251,   247, 18796,   113, 28839,   108, 30266,   123, 23513,    47,
         15922,   165,   242,   223, 33699,    96, 28839,   108, 30266,   123,
         23513,   165, 45865,   162,   252,   114, 28839,   108, 30266,   123,
         20015,    98, 20998,   232],
        [  162,  8955, 38184,   106,   162,   233,   120, 35318, 32573,   238,
         27950,   101, 28839,   108, 30266,   123,   161,   240,   234, 36181,
           106,   162,   247,   114,   163,   253,   111, 28839,   108, 30266,
           123,   163,   255,   231, 16764, 17739,   105, 20998,   116,   164,
           229,   103, 22755,   238, 44165,   233, 27670,   232, 34650,   233,
         31660, 33566,   112, 10310,   241, 37345,   101, 12859,   236, 28839,
           108,   165,   251,    95]])
```

```python
len(data_loader)
```

```plaintext
8
```

```python
import time

optimizer = torch.optim.Adam(gpt_model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
gpt_model.to(device)

EPOCHS = 100

# 记录训练时长
start_time = time.time()
for epoch in range(EPOCHS):
    for i, input_ids in enumerate(data_loader):
        input_ids = input_ids.to(device)

        outputs = gpt_model(
            input_ids, labels=input_ids
        )

        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 每100步打印一次损失值
        if (i + 1) % 4 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                  .format(epoch + 1, EPOCHS, i + 1, len(data_loader), loss.item()))

end_time = time.time()
print('训练完成，耗时：{}'.format(end_time - start_time))
```

```plaintext
Epoch [1/100], Step [4/8], Loss: 0.0813
Epoch [1/100], Step [8/8], Loss: 0.2379
Epoch [2/100], Step [4/8], Loss: 0.1169
Epoch [2/100], Step [8/8], Loss: 0.1320
Epoch [3/100], Step [4/8], Loss: 0.0387
Epoch [3/100], Step [8/8], Loss: 0.0277
Epoch [4/100], Step [4/8], Loss: 0.0213
Epoch [4/100], Step [8/8], Loss: 0.0151
Epoch [5/100], Step [4/8], Loss: 0.0141
Epoch [5/100], Step [8/8], Loss: 0.0060
Epoch [6/100], Step [4/8], Loss: 0.0074
Epoch [6/100], Step [8/8], Loss: 0.0057
Epoch [7/100], Step [4/8], Loss: 0.0198
Epoch [7/100], Step [8/8], Loss: 0.0147
Epoch [8/100], Step [4/8], Loss: 0.0325
Epoch [8/100], Step [8/8], Loss: 0.0140
Epoch [9/100], Step [4/8], Loss: 0.0063
Epoch [9/100], Step [8/8], Loss: 0.0067
Epoch [10/100], Step [4/8], Loss: 0.0051
Epoch [10/100], Step [8/8], Loss: 0.0049
Epoch [11/100], Step [4/8], Loss: 0.0059
Epoch [11/100], Step [8/8], Loss: 0.0027
Epoch [12/100], Step [4/8], Loss: 0.0077
Epoch [12/100], Step [8/8], Loss: 0.0100
Epoch [13/100], Step [4/8], Loss: 0.0366
Epoch [13/100], Step [8/8], Loss: 0.0040
Epoch [14/100], Step [4/8], Loss: 0.0056
Epoch [14/100], Step [8/8], Loss: 0.0024
Epoch [15/100], Step [4/8], Loss: 0.0024
Epoch [15/100], Step [8/8], Loss: 0.0018
Epoch [16/100], Step [4/8], Loss: 0.0094
Epoch [16/100], Step [8/8], Loss: 0.0018
Epoch [17/100], Step [4/8], Loss: 0.0039
Epoch [17/100], Step [8/8], Loss: 0.0023
Epoch [18/100], Step [4/8], Loss: 0.0190
Epoch [18/100], Step [8/8], Loss: 0.0021
Epoch [19/100], Step [4/8], Loss: 0.0637
Epoch [19/100], Step [8/8], Loss: 0.0356
Epoch [20/100], Step [4/8], Loss: 0.0331
Epoch [20/100], Step [8/8], Loss: 0.0356
Epoch [21/100], Step [4/8], Loss: 0.0923
Epoch [21/100], Step [8/8], Loss: 0.0693
Epoch [22/100], Step [4/8], Loss: 0.0753
Epoch [22/100], Step [8/8], Loss: 0.0227
Epoch [23/100], Step [4/8], Loss: 0.0934
Epoch [23/100], Step [8/8], Loss: 0.0758
Epoch [24/100], Step [4/8], Loss: 0.0461
Epoch [24/100], Step [8/8], Loss: 0.0905
Epoch [25/100], Step [4/8], Loss: 0.0539
Epoch [25/100], Step [8/8], Loss: 0.0162
Epoch [26/100], Step [4/8], Loss: 0.0148
Epoch [26/100], Step [8/8], Loss: 0.0032
Epoch [27/100], Step [4/8], Loss: 0.1039
Epoch [27/100], Step [8/8], Loss: 0.0036
Epoch [28/100], Step [4/8], Loss: 0.0278
Epoch [28/100], Step [8/8], Loss: 0.0053
Epoch [29/100], Step [4/8], Loss: 0.0147
Epoch [29/100], Step [8/8], Loss: 0.0399
Epoch [30/100], Step [4/8], Loss: 0.0392
Epoch [30/100], Step [8/8], Loss: 0.0160
Epoch [31/100], Step [4/8], Loss: 0.0111
Epoch [31/100], Step [8/8], Loss: 0.0064
Epoch [32/100], Step [4/8], Loss: 0.0763
Epoch [32/100], Step [8/8], Loss: 0.0038
Epoch [33/100], Step [4/8], Loss: 0.0221
Epoch [33/100], Step [8/8], Loss: 0.0828
Epoch [34/100], Step [4/8], Loss: 0.0052
Epoch [34/100], Step [8/8], Loss: 0.0155
Epoch [35/100], Step [4/8], Loss: 0.0098
Epoch [35/100], Step [8/8], Loss: 0.0023
Epoch [36/100], Step [4/8], Loss: 0.0120
Epoch [36/100], Step [8/8], Loss: 0.0018
Epoch [37/100], Step [4/8], Loss: 0.0043
Epoch [37/100], Step [8/8], Loss: 0.0021
Epoch [38/100], Step [4/8], Loss: 0.0165
Epoch [38/100], Step [8/8], Loss: 0.0032
Epoch [39/100], Step [4/8], Loss: 0.0128
Epoch [39/100], Step [8/8], Loss: 0.0017
Epoch [40/100], Step [4/8], Loss: 0.0029
Epoch [40/100], Step [8/8], Loss: 0.0029
Epoch [41/100], Step [4/8], Loss: 0.0058
Epoch [41/100], Step [8/8], Loss: 0.0016
Epoch [42/100], Step [4/8], Loss: 0.0026
Epoch [42/100], Step [8/8], Loss: 0.0036
Epoch [43/100], Step [4/8], Loss: 0.0065
Epoch [43/100], Step [8/8], Loss: 0.0010
Epoch [44/100], Step [4/8], Loss: 0.0185
Epoch [44/100], Step [8/8], Loss: 0.0011
Epoch [45/100], Step [4/8], Loss: 0.0103
Epoch [45/100], Step [8/8], Loss: 0.0006
Epoch [46/100], Step [4/8], Loss: 0.0046
Epoch [46/100], Step [8/8], Loss: 0.0021
Epoch [47/100], Step [4/8], Loss: 0.0124
Epoch [47/100], Step [8/8], Loss: 0.0011
Epoch [48/100], Step [4/8], Loss: 0.0033
Epoch [48/100], Step [8/8], Loss: 0.0014
Epoch [49/100], Step [4/8], Loss: 0.0027
Epoch [49/100], Step [8/8], Loss: 0.0016
Epoch [50/100], Step [4/8], Loss: 0.0041
Epoch [50/100], Step [8/8], Loss: 0.0064
Epoch [51/100], Step [4/8], Loss: 0.0081
Epoch [51/100], Step [8/8], Loss: 0.0034
Epoch [52/100], Step [4/8], Loss: 0.0045
Epoch [52/100], Step [8/8], Loss: 0.0078
Epoch [53/100], Step [4/8], Loss: 0.0041
Epoch [53/100], Step [8/8], Loss: 0.0010
Epoch [54/100], Step [4/8], Loss: 0.0153
Epoch [54/100], Step [8/8], Loss: 0.0013
Epoch [55/100], Step [4/8], Loss: 0.0182
Epoch [55/100], Step [8/8], Loss: 0.0351
Epoch [56/100], Step [4/8], Loss: 0.0040
Epoch [56/100], Step [8/8], Loss: 0.0012
Epoch [57/100], Step [4/8], Loss: 0.0039
Epoch [57/100], Step [8/8], Loss: 0.0032
Epoch [58/100], Step [4/8], Loss: 0.0018
Epoch [58/100], Step [8/8], Loss: 0.0045
Epoch [59/100], Step [4/8], Loss: 0.0040
Epoch [59/100], Step [8/8], Loss: 0.0082
Epoch [60/100], Step [4/8], Loss: 0.0064
Epoch [60/100], Step [8/8], Loss: 0.0019
Epoch [61/100], Step [4/8], Loss: 0.0012
Epoch [61/100], Step [8/8], Loss: 0.0059
Epoch [62/100], Step [4/8], Loss: 0.0073
Epoch [62/100], Step [8/8], Loss: 0.0015
Epoch [63/100], Step [4/8], Loss: 0.0013
Epoch [63/100], Step [8/8], Loss: 0.0043
Epoch [64/100], Step [4/8], Loss: 0.0020
Epoch [64/100], Step [8/8], Loss: 0.0012
Epoch [65/100], Step [4/8], Loss: 0.0008
Epoch [65/100], Step [8/8], Loss: 0.0004
Epoch [66/100], Step [4/8], Loss: 0.0008
Epoch [66/100], Step [8/8], Loss: 0.0012
Epoch [67/100], Step [4/8], Loss: 0.0006
Epoch [67/100], Step [8/8], Loss: 0.0004
Epoch [68/100], Step [4/8], Loss: 0.0009
Epoch [68/100], Step [8/8], Loss: 0.0006
Epoch [69/100], Step [4/8], Loss: 0.0007
Epoch [69/100], Step [8/8], Loss: 0.0005
Epoch [70/100], Step [4/8], Loss: 0.0027
Epoch [70/100], Step [8/8], Loss: 0.0004
Epoch [71/100], Step [4/8], Loss: 0.0005
Epoch [71/100], Step [8/8], Loss: 0.0002
Epoch [72/100], Step [4/8], Loss: 0.0022
Epoch [72/100], Step [8/8], Loss: 0.0004
Epoch [73/100], Step [4/8], Loss: 0.0006
Epoch [73/100], Step [8/8], Loss: 0.0004
Epoch [74/100], Step [4/8], Loss: 0.0004
Epoch [74/100], Step [8/8], Loss: 0.0004
Epoch [75/100], Step [4/8], Loss: 0.0006
Epoch [75/100], Step [8/8], Loss: 0.0003
Epoch [76/100], Step [4/8], Loss: 0.0022
Epoch [76/100], Step [8/8], Loss: 0.0005
Epoch [77/100], Step [4/8], Loss: 0.0006
Epoch [77/100], Step [8/8], Loss: 0.0003
Epoch [78/100], Step [4/8], Loss: 0.0005
Epoch [78/100], Step [8/8], Loss: 0.0004
Epoch [79/100], Step [4/8], Loss: 0.0007
Epoch [79/100], Step [8/8], Loss: 0.0002
Epoch [80/100], Step [4/8], Loss: 0.0003
Epoch [80/100], Step [8/8], Loss: 0.0004
Epoch [81/100], Step [4/8], Loss: 0.0004
Epoch [81/100], Step [8/8], Loss: 0.0003
Epoch [82/100], Step [4/8], Loss: 0.0038
Epoch [82/100], Step [8/8], Loss: 0.0004
Epoch [83/100], Step [4/8], Loss: 0.0008
Epoch [83/100], Step [8/8], Loss: 0.0003
Epoch [84/100], Step [4/8], Loss: 0.0009
Epoch [84/100], Step [8/8], Loss: 0.0003
Epoch [85/100], Step [4/8], Loss: 0.0013
Epoch [85/100], Step [8/8], Loss: 0.0002
Epoch [86/100], Step [4/8], Loss: 0.0362
Epoch [86/100], Step [8/8], Loss: 0.0115
Epoch [87/100], Step [4/8], Loss: 0.0058
Epoch [87/100], Step [8/8], Loss: 0.0092
Epoch [88/100], Step [4/8], Loss: 0.0036
Epoch [88/100], Step [8/8], Loss: 0.0023
Epoch [89/100], Step [4/8], Loss: 0.0025
Epoch [89/100], Step [8/8], Loss: 0.0078
Epoch [90/100], Step [4/8], Loss: 0.0462
Epoch [90/100], Step [8/8], Loss: 0.0096
Epoch [91/100], Step [4/8], Loss: 0.0115
Epoch [91/100], Step [8/8], Loss: 0.0026
Epoch [92/100], Step [4/8], Loss: 0.0167
Epoch [92/100], Step [8/8], Loss: 0.0106
Epoch [93/100], Step [4/8], Loss: 0.0868
Epoch [93/100], Step [8/8], Loss: 0.0428
Epoch [94/100], Step [4/8], Loss: 0.0861
Epoch [94/100], Step [8/8], Loss: 0.2409
Epoch [95/100], Step [4/8], Loss: 0.0592
Epoch [95/100], Step [8/8], Loss: 0.2358
Epoch [96/100], Step [4/8], Loss: 0.1064
Epoch [96/100], Step [8/8], Loss: 0.0483
Epoch [97/100], Step [4/8], Loss: 0.1448
Epoch [97/100], Step [8/8], Loss: 0.1269
Epoch [98/100], Step [4/8], Loss: 0.1560
Epoch [98/100], Step [8/8], Loss: 0.0425
Epoch [99/100], Step [4/8], Loss: 0.2810
Epoch [99/100], Step [8/8], Loss: 0.0648
Epoch [100/100], Step [4/8], Loss: 0.1198
Epoch [100/100], Step [8/8], Loss: 0.0638
开始训练时间：1752651723.905466
结束训练时间：1752651723.905466
训练完成，耗时：32.85186696052551
```

```python

# 生成函数
def generate(sentence, max_length=500):
    input_ids = gpt_tokenizer.encode(sentence, return_tensors='pt', add_special_tokens=False)
    input_ids = input_ids.to(device)
    output = gpt_model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id=gpt_tokenizer.eos_token_id,
        do_sample=True,
    )
    return gpt_tokenizer.decode(output[0])


print(generate("PVC片材"))
```

```plaintext
PVC片材石塑卷板、PVC卷材、PVC防静电地板、PVC锁扣地板、装领�VC地板、箤证�PVC地板、PVC地板、PVC地靦����向，防饲���地板、PVC地板、PVC地板、PVC地板、PVC地靝��高�市�面��，PVC地板、PVC地杆�核�导��司PVC地��PVC地板、PVC地板、PVC地板等，地板�地板�超�PVC地蓁�，地板��厂地靝���地板，超�������以靝��市Ｘ�导各�栆PVC地板、PVC地板、PVC地板�各��PVC地板，时��吷板，服地板，以靝���，������仝�PVC地心�地������学��仂�市�厥��超�地杦��以各�栆PVC地板，�期����PVC地板��发�各��栆PVC�逄�琦�PVC地板�PVC地板�、PVC地板，地板��心�高�実����
```