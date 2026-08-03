# 30、PyTorch版Transformer机器翻译实战

```python
from collections import Counter

import jieba
import torch
import torch.nn as nn
import torch.optim as optim

# 自定义简单数据集
data = [
    ("你好，今天天气真好！", "Hello, the weather is nice today!"),
    ("你吃饭了吗？", "Have you eaten yet?"),
    ("深度学习很有趣。", "Deep learning is interesting."),
    ("我们一起学习吧。", "Let's study together."),
    ("这是一个测试例子。", "This is a test example.")
]


# 中文分词函数
def chinese_split(text):
    return list(jieba.cut(text))  # 使用结巴分词


# 英文分词函数
def english_split(text):
    return text.lower().split()


# 处理原始数据
chinese_sentences = [chinese_split(pair[0]) for pair in data]
english_sentences = [english_split(pair[1]) for pair in data]

chinese_sentences, english_sentences
```

```plaintext
([['你好', '，', '今天天气', '真', '好', '！'],
  ['你', '吃饭', '了', '吗', '？'],
  ['深度', '学习', '很', '有趣', '。'],
  ['我们', '一起', '学习', '吧', '。'],
  ['这是', '一个', '测试', '例子', '。']],
 [['hello,', 'the', 'weather', 'is', 'nice', 'today!'],
  ['have', 'you', 'eaten', 'yet?'],
  ['deep', 'learning', 'is', 'interesting.'],
  ["let's", 'study', 'together.'],
  ['this', 'is', 'a', 'test', 'example.']])
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
zh_vocab, zh_word2idx = build_vocab([sentence for sentence in chinese_sentences])

en_vocab, en_word2idx = build_vocab([sentence for sentence in english_sentences])

# print(zh_vocab)
# print(en_vocab)
print(zh_word2idx)
print(en_word2idx)
```

```plaintext
{'<pad>': 0, '<bos>': 1, '<eos>': 2, '<unk>': 3, '你好': 4, '，': 5, '今天天气': 6, '真': 7, '好': 8, '！': 9, '你': 10, '吃饭': 11, '了': 12, '吗': 13, '？': 14, '深度': 15, '学习': 16, '很': 17, '有趣': 18, '。': 19, '我们': 20, '一起': 21, '吧': 22, '这是': 23, '一个': 24, '测试': 25, '例子': 26}
{'<pad>': 0, '<bos>': 1, '<eos>': 2, '<unk>': 3, 'hello,': 4, 'the': 5, 'weather': 6, 'is': 7, 'nice': 8, 'today!': 9, 'have': 10, 'you': 11, 'eaten': 12, 'yet?': 13, 'deep': 14, 'learning': 15, 'interesting.': 16, "let's": 17, 'study': 18, 'together.': 19, 'this': 20, 'a': 21, 'test': 22, 'example.': 23}
```

```python
# 参数设置
ZH_VOCAB_SIZE = len(zh_vocab)
EN_VOCAB_SIZE = len(en_vocab)
HIDDEN_SIZE = 256
BATCH_SIZE = 2
LEARNING_RATE = 0.005


def tokenize(words, word2idx):
    # 如果某个词在字典中找不到，则用'<unk>'的索引代替
    return [word2idx.get(word, word2idx['<unk>']) for word in words]


processed_data_ch = []
processed_data_en = []
for ch, en in zip(chinese_sentences, english_sentences):
    # ch，en分别是一个中文句子和对应的英文句子
    # 在每个句子的前面加上'<bos>'，在每个句子的后面加上'<eos>'，这样大模型才能知道什么时候停止生成句子
    ch_numerical = tokenize(ch, zh_word2idx)
    en_numerical = [en_word2idx['<bos>']] + tokenize(en, en_word2idx) + [en_word2idx['<eos>']]
    processed_data_ch.append(torch.LongTensor(ch_numerical))
    processed_data_en.append(torch.LongTensor(en_numerical))

# print(processed_data_ch)
processed_data_en
```

```plaintext
[tensor([1, 4, 5, 6, 7, 8, 9, 2]),
 tensor([ 1, 10, 11, 12, 13,  2]),
 tensor([ 1, 14, 15,  7, 16,  2]),
 tensor([ 1, 17, 18, 19,  2]),
 tensor([ 1, 20,  7, 21, 22, 23,  2])]
```

```python
processed_data_ch_pad = nn.utils.rnn.pad_sequence(processed_data_ch, batch_first=True,
                                                  padding_value=zh_word2idx['<pad>'])
processed_data_ch_pad
```

```plaintext
tensor([[ 4,  5,  6,  7,  8,  9],
        [10, 11, 12, 13, 14,  0],
        [15, 16, 17, 18, 19,  0],
        [20, 21, 16, 22, 19,  0],
        [23, 24, 25, 26, 19,  0]])
```

```python
# 对processed_data进行数据填充，对齐长度
processed_data_en_pad = nn.utils.rnn.pad_sequence(processed_data_en, batch_first=True,
                                                  padding_value=en_word2idx['<pad>'])
processed_data_en_pad
```

```plaintext
tensor([[ 1,  4,  5,  6,  7,  8,  9,  2],
        [ 1, 10, 11, 12, 13,  2,  0,  0],
        [ 1, 14, 15,  7, 16,  2,  0,  0],
        [ 1, 17, 18, 19,  2,  0,  0,  0],
        [ 1, 20,  7, 21, 22, 23,  2,  0]])
```

```python

from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(processed_data_ch_pad, processed_data_en_pad)
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

for src, trg in dataloader:
    print(src)
    print(trg)
    break
```

```plaintext
tensor([[4, 5, 6, 7, 8, 9]])
tensor([[1, 4, 5, 6, 7, 8, 9, 2]])
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
        self.encoder_embedding = nn.Embedding(len(zh_vocab), d_model)
        self.decoder_embedding = nn.Embedding(len(en_vocab), d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        self.transformer = nn.Transformer(d_model=d_model, dim_feedforward=dim_feedforward, nhead=nhead,
                                          num_encoder_layers=num_encoder_layers,
                                          num_decoder_layers=num_decoder_layers, batch_first=True, dropout=0)
        self.fc = nn.Linear(d_model, len(en_vocab))

    def forward(self, zh_inputs, en_inputs):

        batch_size, en_seq_len = en_inputs.shape
        # mask = torch.tril(torch.ones(en_seq_len, en_seq_len))
        mask = nn.Transformer.generate_square_subsequent_mask(en_seq_len)

        # 词嵌入和位置编码
        encoder_input = self.pos_encoder(self.encoder_embedding(zh_inputs))
        decoder_input = self.pos_encoder(self.decoder_embedding(en_inputs))

        output = self.transformer(
            src=encoder_input, tgt=decoder_input,
            tgt_mask=mask
        )

        return self.fc(output)
```

```python
model = ZhouyuModel(d_model=128, dim_feedforward=2048, nhead=8, num_encoder_layers=2, num_decoder_layers=2)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss(ignore_index=en_word2idx['<pad>'])
```

```python
# 打印一下model的参数个数
print(sum(p.numel() for p in model.parameters()))
```

```plaintext
2514840
```

```python
for epoch in range(20):
    # input： tensor([[4, 5, 6, 7, 8, 9]])
    # target：tensor([[1, 4, 5, 6, 7, 8, 9, 2]])
    for input, target in dataloader:
        # 准备解码器输入输出，其实这一步可以在数据处理时做掉
        decoder_input = target[:, :-1]  # 移除最后一个token  tensor([[1, 4, 5, 6, 7, 8, 9]])
        decoder_target = target[:, 1:]  # 移除第一个token    tensor([[4, 5, 6, 7, 8, 9, 2]])

        decoder_outputs = model(input, decoder_input)

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
Epoch 1, Loss: 3.3264
Epoch 1, Loss: 3.7421
Epoch 1, Loss: 3.7243
Epoch 1, Loss: 4.0434
Epoch 1, Loss: 3.9274
Epoch 2, Loss: 2.8441
Epoch 2, Loss: 2.6646
Epoch 2, Loss: 2.3883
Epoch 2, Loss: 2.7236
Epoch 2, Loss: 3.2953
Epoch 3, Loss: 2.5373
Epoch 3, Loss: 2.4220
Epoch 3, Loss: 1.8835
Epoch 3, Loss: 1.9247
Epoch 3, Loss: 2.4776
Epoch 4, Loss: 1.0088
Epoch 4, Loss: 1.3849
Epoch 4, Loss: 1.2230
Epoch 4, Loss: 1.0992
Epoch 4, Loss: 1.6393
Epoch 5, Loss: 0.7535
Epoch 5, Loss: 0.9344
Epoch 5, Loss: 0.7792
Epoch 5, Loss: 0.6252
Epoch 5, Loss: 1.4751
Epoch 6, Loss: 0.5453
Epoch 6, Loss: 0.4671
Epoch 6, Loss: 0.6886
Epoch 6, Loss: 0.6248
Epoch 6, Loss: 0.5865
Epoch 7, Loss: 0.3908
Epoch 7, Loss: 0.4004
Epoch 7, Loss: 0.5349
Epoch 7, Loss: 0.4084
Epoch 7, Loss: 0.4034
Epoch 8, Loss: 0.3308
Epoch 8, Loss: 0.2888
Epoch 8, Loss: 0.3510
Epoch 8, Loss: 0.2535
Epoch 8, Loss: 0.3579
Epoch 9, Loss: 0.1949
Epoch 9, Loss: 0.2005
Epoch 9, Loss: 0.2476
Epoch 9, Loss: 0.1317
Epoch 9, Loss: 0.1958
Epoch 10, Loss: 0.1357
Epoch 10, Loss: 0.1157
Epoch 10, Loss: 0.1599
Epoch 10, Loss: 0.0894
Epoch 10, Loss: 0.0979
Epoch 11, Loss: 0.1076
Epoch 11, Loss: 0.0825
Epoch 11, Loss: 0.0874
Epoch 11, Loss: 0.0654
Epoch 11, Loss: 0.0662
Epoch 12, Loss: 0.0707
Epoch 12, Loss: 0.0580
Epoch 12, Loss: 0.0653
Epoch 12, Loss: 0.0452
Epoch 12, Loss: 0.0508
Epoch 13, Loss: 0.0490
Epoch 13, Loss: 0.0426
Epoch 13, Loss: 0.0449
Epoch 13, Loss: 0.0357
Epoch 13, Loss: 0.0402
Epoch 14, Loss: 0.0392
Epoch 14, Loss: 0.0338
Epoch 14, Loss: 0.0359
Epoch 14, Loss: 0.0299
Epoch 14, Loss: 0.0342
Epoch 15, Loss: 0.0327
Epoch 15, Loss: 0.0283
Epoch 15, Loss: 0.0305
Epoch 15, Loss: 0.0256
Epoch 15, Loss: 0.0299
Epoch 16, Loss: 0.0280
Epoch 16, Loss: 0.0248
Epoch 16, Loss: 0.0272
Epoch 16, Loss: 0.0230
Epoch 16, Loss: 0.0261
Epoch 17, Loss: 0.0251
Epoch 17, Loss: 0.0223
Epoch 17, Loss: 0.0250
Epoch 17, Loss: 0.0210
Epoch 17, Loss: 0.0235
Epoch 18, Loss: 0.0232
Epoch 18, Loss: 0.0207
Epoch 18, Loss: 0.0231
Epoch 18, Loss: 0.0196
Epoch 18, Loss: 0.0217
Epoch 19, Loss: 0.0217
Epoch 19, Loss: 0.0193
Epoch 19, Loss: 0.0215
Epoch 19, Loss: 0.0184
Epoch 19, Loss: 0.0203
Epoch 20, Loss: 0.0204
Epoch 20, Loss: 0.0182
Epoch 20, Loss: 0.0203
Epoch 20, Loss: 0.0175
Epoch 20, Loss: 0.0190
```

```python
# 翻译函数

def translate(sentence, model):
    zh_tokens = torch.LongTensor(tokenize(chinese_split(sentence), zh_word2idx))
    encoder_input = model.pos_encoder(model.encoder_embedding(zh_tokens).unsqueeze(0))
    encoder_outputs = model.transformer.encoder(encoder_input)

    decoder_inputs = [en_word2idx['<bos>']]

    for _ in range(50):
        with torch.no_grad():
            decoder_input = model.pos_encoder(model.decoder_embedding(torch.LongTensor(decoder_inputs)).unsqueeze(0))
            decoder_output = model.transformer.decoder(tgt=decoder_input, memory=encoder_outputs, tgt_mask=None)
            output = model.fc(decoder_output)
            pred_token = output[:, -1, :].argmax().item()
            decoder_inputs.append(pred_token)
            if pred_token == en_word2idx['<eos>']:
                break

    return ' '.join([en_vocab[idx] for idx in decoder_inputs[1:-1]])


# 测试翻译
test_sentence = "我们一起学习"
print(translate(test_sentence, model))
```

```plaintext
let's study together.
```