# 31、PyTorch版Transformer古诗生成实战

```python
from collections import Counter

import torch
import torch.nn as nn
import torch.optim as optim

poem_data = [
    ("登鹳雀楼", "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"),
    ("静夜思", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("春晓", "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。"),
    ("相思", "红豆生南国，春来发几枝。愿君多采撷，此物最相思。"),
    ("江雪", "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。")
]
```

```python
# 数据预处理
def preprocess_data(data):
    src_sentences = []
    tgt_sentences = []

    # 中文按字符分割
    for src, tgt in data:
        src_tokens = list(src)
        tgt_tokens = list(tgt)
        src_sentences.append(src_tokens)
        tgt_sentences.append(tgt_tokens)
    return src_sentences, tgt_sentences

src_sentences, tgt_sentences = preprocess_data(poem_data)
src_sentences, tgt_sentences
```

```plaintext
([['登', '鹳', '雀', '楼'], ['静', '夜', '思'], ['春', '晓'], ['相', '思'], ['江', '雪']],
 [['白',
   '日',
   '依',
   '山',
   '尽',
   '，',
   '黄',
   '河',
   '入',
   '海',
   '流',
   '。',
   '欲',
   '穷',
   '千',
   '里',
   '目',
   '，',
   '更',
   '上',
   '一',
   '层',
   '楼',
   '。'],
  ['床',
   '前',
   '明',
   '月',
   '光',
   '，',
   '疑',
   '是',
   '地',
   '上',
   '霜',
   '。',
   '举',
   '头',
   '望',
   '明',
   '月',
   '，',
   '低',
   '头',
   '思',
   '故',
   '乡',
   '。'],
  ['春',
   '眠',
   '不',
   '觉',
   '晓',
   '，',
   '处',
   '处',
   '闻',
   '啼',
   '鸟',
   '。',
   '夜',
   '来',
   '风',
   '雨',
   '声',
   '，',
   '花',
   '落',
   '知',
   '多',
   '少',
   '。'],
  ['红',
   '豆',
   '生',
   '南',
   '国',
   '，',
   '春',
   '来',
   '发',
   '几',
   '枝',
   '。',
   '愿',
   '君',
   '多',
   '采',
   '撷',
   '，',
   '此',
   '物',
   '最',
   '相',
   '思',
   '。'],
  ['千',
   '山',
   '鸟',
   '飞',
   '绝',
   '，',
   '万',
   '径',
   '人',
   '踪',
   '灭',
   '。',
   '孤',
   '舟',
   '蓑',
   '笠',
   '翁',
   '，',
   '独',
   '钓',
   '寒',
   '江',
   '雪',
   '。']])
```

```python
# 处理特殊符号
special_tokens = ['<pad>', '<bos>', '<eos>', '<unk>']


# 构建词汇表
def build_vocab(sentences):
    counter = Counter()

    for sentence in sentences:
        for word in sentence:
            counter[word] += 1

    vocab = special_tokens.copy()

    for word, count in counter.items():
        if word not in special_tokens:
            vocab.append(word)

    word2idx = {word: idx for idx, word in enumerate(vocab)}
    return vocab, word2idx


# 构建中英文词汇表
src_vocab, src_word2idx = build_vocab([sentence for sentence in src_sentences])
tgt_vocab, tgt_word2idx = build_vocab([sentence for sentence in tgt_sentences])

# print(src_vocab)
# print(tgt_vocab)
print(src_word2idx)
print(tgt_word2idx)
```

```plaintext
{'<pad>': 0, '<bos>': 1, '<eos>': 2, '<unk>': 3, '登': 4, '鹳': 5, '雀': 6, '楼': 7, '静': 8, '夜': 9, '思': 10, '春': 11, '晓': 12, '相': 13, '江': 14, '雪': 15}
{'<pad>': 0, '<bos>': 1, '<eos>': 2, '<unk>': 3, '白': 4, '日': 5, '依': 6, '山': 7, '尽': 8, '，': 9, '黄': 10, '河': 11, '入': 12, '海': 13, '流': 14, '。': 15, '欲': 16, '穷': 17, '千': 18, '里': 19, '目': 20, '更': 21, '上': 22, '一': 23, '层': 24, '楼': 25, '床': 26, '前': 27, '明': 28, '月': 29, '光': 30, '疑': 31, '是': 32, '地': 33, '霜': 34, '举': 35, '头': 36, '望': 37, '低': 38, '思': 39, '故': 40, '乡': 41, '春': 42, '眠': 43, '不': 44, '觉': 45, '晓': 46, '处': 47, '闻': 48, '啼': 49, '鸟': 50, '夜': 51, '来': 52, '风': 53, '雨': 54, '声': 55, '花': 56, '落': 57, '知': 58, '多': 59, '少': 60, '红': 61, '豆': 62, '生': 63, '南': 64, '国': 65, '发': 66, '几': 67, '枝': 68, '愿': 69, '君': 70, '采': 71, '撷': 72, '此': 73, '物': 74, '最': 75, '相': 76, '飞': 77, '绝': 78, '万': 79, '径': 80, '人': 81, '踪': 82, '灭': 83, '孤': 84, '舟': 85, '蓑': 86, '笠': 87, '翁': 88, '独': 89, '钓': 90, '寒': 91, '江': 92, '雪': 93}
```

```python
# 参数设置
SRC_VOCAB_SIZE = len(src_vocab)
TGT_VOCAB_SIZE = len(tgt_vocab)
D_MODEL = 128
BATCH_SIZE = 2
LEARNING_RATE = 0.005


def tokenize(words, word2idx):
    # 如果某个词在字典中找不到，则用'<unk>'的索引代替
    return [word2idx.get(word, word2idx['<unk>']) for word in words]


processed_data_src = []
processed_data_tgt = []
for src, tgt in zip(src_sentences, tgt_sentences):
    src_numerical = tokenize(src, src_word2idx)
    tgt_numerical = [tgt_word2idx['<bos>']] + tokenize(tgt, tgt_word2idx) + [tgt_word2idx['<eos>']]
    processed_data_src.append(torch.LongTensor(src_numerical))
    processed_data_tgt.append(torch.LongTensor(tgt_numerical))

processed_data_tgt
```

```plaintext
[tensor([ 1,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          9, 21, 22, 23, 24, 25, 15,  2]),
 tensor([ 1, 26, 27, 28, 29, 30,  9, 31, 32, 33, 22, 34, 15, 35, 36, 37, 28, 29,
          9, 38, 36, 39, 40, 41, 15,  2]),
 tensor([ 1, 42, 43, 44, 45, 46,  9, 47, 47, 48, 49, 50, 15, 51, 52, 53, 54, 55,
          9, 56, 57, 58, 59, 60, 15,  2]),
 tensor([ 1, 61, 62, 63, 64, 65,  9, 42, 52, 66, 67, 68, 15, 69, 70, 59, 71, 72,
          9, 73, 74, 75, 76, 39, 15,  2]),
 tensor([ 1, 18,  7, 50, 77, 78,  9, 79, 80, 81, 82, 83, 15, 84, 85, 86, 87, 88,
          9, 89, 90, 91, 92, 93, 15,  2])]
```

```python
processed_data_src_pad = nn.utils.rnn.pad_sequence(processed_data_src, batch_first=True,
                                                  padding_value=src_word2idx['<pad>'])
processed_data_src_pad
```

```plaintext
tensor([[ 4,  5,  6,  7],
        [ 8,  9, 10,  0],
        [11, 12,  0,  0],
        [13, 10,  0,  0],
        [14, 15,  0,  0]])
```

```python
# 对processed_data进行数据填充，对齐长度
processed_data_tgt_pad = nn.utils.rnn.pad_sequence(processed_data_tgt, batch_first=True,
                                                  padding_value=tgt_word2idx['<pad>'])
processed_data_tgt_pad
```

```plaintext
tensor([[ 1,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          9, 21, 22, 23, 24, 25, 15,  2],
        [ 1, 26, 27, 28, 29, 30,  9, 31, 32, 33, 22, 34, 15, 35, 36, 37, 28, 29,
          9, 38, 36, 39, 40, 41, 15,  2],
        [ 1, 42, 43, 44, 45, 46,  9, 47, 47, 48, 49, 50, 15, 51, 52, 53, 54, 55,
          9, 56, 57, 58, 59, 60, 15,  2],
        [ 1, 61, 62, 63, 64, 65,  9, 42, 52, 66, 67, 68, 15, 69, 70, 59, 71, 72,
          9, 73, 74, 75, 76, 39, 15,  2],
        [ 1, 18,  7, 50, 77, 78,  9, 79, 80, 81, 82, 83, 15, 84, 85, 86, 87, 88,
          9, 89, 90, 91, 92, 93, 15,  2]])
```

```python

from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(processed_data_src_pad, processed_data_tgt_pad)
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

for src, tgt in dataloader:
    print(src)
    print(tgt)
    break
```

```plaintext
tensor([[4, 5, 6, 7]])
tensor([[ 1,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          9, 21, 22, 23, 24, 25, 15,  2]])
```

```python
# 位置编码
# 大都督周瑜（我的微信: it_zhouyu）

import math


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_seq_len=128):
        super().__init__()
        self.pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        self.pe[:, 0::2] = torch.sin(position * div_term)
        self.pe[:, 1::2] = torch.cos(position * div_term)

    def forward(self, x):
        x = x + self.pe[:x.size(1), :]
        return x
```

```python
class ZhouyuModel(nn.Module):
    def __init__(self, d_model, dim_feedforward, nhead, num_encoder_layers, num_decoder_layers):
        super().__init__()
        self.encoder_embedding = nn.Embedding(len(src_vocab), d_model)
        self.decoder_embedding = nn.Embedding(len(tgt_vocab), d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        self.transformer = nn.Transformer(d_model=d_model, dim_feedforward=dim_feedforward, nhead=nhead,
                                          num_encoder_layers=num_encoder_layers,
                                          num_decoder_layers=num_decoder_layers, batch_first=True, dropout=0)
        self.fc = nn.Linear(d_model, len(tgt_vocab))

    def forward(self, src, tgt):

        batch_size, en_seq_len = tgt.shape
        # mask = torch.tril(torch.ones(en_seq_len, en_seq_len))
        mask = nn.Transformer.generate_square_subsequent_mask(en_seq_len)

        # 词嵌入和位置编码
        encoder_input = self.pos_encoder(self.encoder_embedding(src))
        decoder_input = self.pos_encoder(self.decoder_embedding(tgt))

        output = self.transformer(
            src=encoder_input, tgt=decoder_input,
            tgt_mask=mask
        )

        return self.fc(output)
```

```python
model = ZhouyuModel(d_model=128, dim_feedforward=2048, nhead=8, num_encoder_layers=2, num_decoder_layers=2)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss(ignore_index=tgt_word2idx['<pad>'])
```

```python
# 打印一下model的参数个数
print(sum(p.numel() for p in model.parameters()))
```

```plaintext
2531422
```

```python
for epoch in range(20):
    for src, tgt in dataloader:
        # 准备解码器输入输出，其实这一步可以在数据处理时做掉
        decoder_input = tgt[:, :-1]  # 移除最后一个token  tensor([[1, 4, 5, 6, 7, 8, 9]])
        decoder_target = tgt[:, 1:]  # 移除第一个token    tensor([[4, 5, 6, 7, 8, 9, 2]])

        decoder_outputs = model(src, decoder_input)

        # 计算损失
        loss = criterion(
            # decoder_output本来是(batch_size, seq_len, vocab_size)，变成(batch_size * seq_len, vocab_size)
            # decoder_target本来是(batch_size, seq_len)，变成(batch_size * seq_len)
            decoder_outputs.view(-1, decoder_outputs.size(-1)),
            decoder_target.view(-1)
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')
```

```plaintext
Epoch 1, Loss: 4.8608
Epoch 1, Loss: 4.5106
Epoch 1, Loss: 4.7312
Epoch 1, Loss: 4.9179
Epoch 1, Loss: 4.8792
Epoch 2, Loss: 4.2399
Epoch 2, Loss: 4.0221
Epoch 2, Loss: 4.1562
Epoch 2, Loss: 4.3885
Epoch 2, Loss: 4.5121
Epoch 3, Loss: 4.0885
Epoch 3, Loss: 3.8313
Epoch 3, Loss: 3.8590
Epoch 3, Loss: 3.8335
Epoch 3, Loss: 3.9192
Epoch 4, Loss: 2.7080
Epoch 4, Loss: 3.3350
Epoch 4, Loss: 3.0133
Epoch 4, Loss: 3.3189
Epoch 4, Loss: 3.4096
Epoch 5, Loss: 1.9106
Epoch 5, Loss: 2.1204
Epoch 5, Loss: 2.2081
Epoch 5, Loss: 2.7348
Epoch 5, Loss: 2.3861
Epoch 6, Loss: 1.4321
Epoch 6, Loss: 1.5706
Epoch 6, Loss: 1.6909
Epoch 6, Loss: 1.8521
Epoch 6, Loss: 1.8491
Epoch 7, Loss: 1.3301
Epoch 7, Loss: 1.2691
Epoch 7, Loss: 1.1711
Epoch 7, Loss: 1.5945
Epoch 7, Loss: 1.4547
Epoch 8, Loss: 0.8385
Epoch 8, Loss: 0.9792
Epoch 8, Loss: 1.0672
Epoch 8, Loss: 1.1525
Epoch 8, Loss: 0.9828
Epoch 9, Loss: 0.7181
Epoch 9, Loss: 0.7519
Epoch 9, Loss: 0.6820
Epoch 9, Loss: 0.7836
Epoch 9, Loss: 0.6863
Epoch 10, Loss: 0.5208
Epoch 10, Loss: 0.6068
Epoch 10, Loss: 0.5296
Epoch 10, Loss: 0.5496
Epoch 10, Loss: 0.5077
Epoch 11, Loss: 0.3932
Epoch 11, Loss: 0.4355
Epoch 11, Loss: 0.3899
Epoch 11, Loss: 0.3873
Epoch 11, Loss: 0.3838
Epoch 12, Loss: 0.3101
Epoch 12, Loss: 0.3185
Epoch 12, Loss: 0.3162
Epoch 12, Loss: 0.3054
Epoch 12, Loss: 0.3056
Epoch 13, Loss: 0.2455
Epoch 13, Loss: 0.2383
Epoch 13, Loss: 0.2658
Epoch 13, Loss: 0.2413
Epoch 13, Loss: 0.2365
Epoch 14, Loss: 0.2053
Epoch 14, Loss: 0.2071
Epoch 14, Loss: 0.2256
Epoch 14, Loss: 0.2010
Epoch 14, Loss: 0.2010
Epoch 15, Loss: 0.1750
Epoch 15, Loss: 0.1790
Epoch 15, Loss: 0.2034
Epoch 15, Loss: 0.1758
Epoch 15, Loss: 0.1776
Epoch 16, Loss: 0.1535
Epoch 16, Loss: 0.1565
Epoch 16, Loss: 0.1871
Epoch 16, Loss: 0.1584
Epoch 16, Loss: 0.1560
Epoch 17, Loss: 0.1425
Epoch 17, Loss: 0.1423
Epoch 17, Loss: 0.1718
Epoch 17, Loss: 0.1455
Epoch 17, Loss: 0.1401
Epoch 18, Loss: 0.1331
Epoch 18, Loss: 0.1295
Epoch 18, Loss: 0.1583
Epoch 18, Loss: 0.1347
Epoch 18, Loss: 0.1317
Epoch 19, Loss: 0.1227
Epoch 19, Loss: 0.1176
Epoch 19, Loss: 0.1606
Epoch 19, Loss: 0.1249
Epoch 19, Loss: 0.1218
Epoch 20, Loss: 0.1139
Epoch 20, Loss: 0.1064
Epoch 20, Loss: 0.2677
Epoch 20, Loss: 0.1159
Epoch 20, Loss: 0.1117
```

```python
# 生成函数
def translate(sentence, model):
    src_tokens = torch.LongTensor(tokenize(list(sentence), src_word2idx))
    encoder_input = model.pos_encoder(model.encoder_embedding(src_tokens).unsqueeze(0))
    encoder_outputs = model.transformer.encoder(encoder_input)

    decoder_inputs = [tgt_word2idx['<bos>']]

    for _ in range(50):
        with torch.no_grad():
            decoder_input = model.pos_encoder(model.decoder_embedding(torch.LongTensor(decoder_inputs)).unsqueeze(0))
            decoder_output = model.transformer.decoder(tgt=decoder_input, memory=encoder_outputs, tgt_mask=None)
            output = model.fc(decoder_output)
            pred_token = output[:, -1, :].argmax().item()
            decoder_inputs.append(pred_token)
            if pred_token == tgt_word2idx['<eos>']:
                break

    return ''.join([tgt_vocab[idx] for idx in decoder_inputs[1:-1]])


# 测试翻译
test_sentence = "春晓"
print(translate(test_sentence, model))
```

```plaintext
春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。
```