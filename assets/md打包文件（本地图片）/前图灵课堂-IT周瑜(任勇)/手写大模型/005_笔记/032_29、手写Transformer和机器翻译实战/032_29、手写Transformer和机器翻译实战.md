# 29、手写Transformer和机器翻译实战

```python
import torch
import torch.nn as nn

batch_size = 2
zh_seq_len = 5
en_seq_len = 6
d_model = 512  # 词向量的长度
vocab_size = 100

# 生成两个句子，每个句子有5个词
zh_sentences = torch.randint(0, vocab_size, (batch_size, zh_seq_len))
en_sentences = torch.randint(0, vocab_size, (batch_size, en_seq_len))
zh_sentences, en_sentences
```

```plaintext
(tensor([[60, 34, 55, 99, 21],
         [58, 64, 42, 86, 41]]),
 tensor([[22, 81, 96, 42, 79, 14],
         [83, 50,  6, 16, 14, 29]]))
```

```python
# 词嵌入层
encoder_embedding = nn.Embedding(vocab_size, d_model)
decoder_embedding = nn.Embedding(vocab_size, d_model)

encoder_embeddings = encoder_embedding(zh_sentences)
decoder_embeddings = decoder_embedding(en_sentences)
encoder_embeddings.shape, decoder_embeddings.shape
```

```plaintext
(torch.Size([2, 5, 512]), torch.Size([2, 6, 512]))
```

```python
import math

# 位置编码
# 位置编码只跟位置有关，和具体位置上输入的数据无关
max_seq_len = 128
pe = torch.zeros(max_seq_len, d_model)
position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)
div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
pe[:, 0::2] = torch.sin(position * div_term)
pe[:, 1::2] = torch.cos(position * div_term)
pe
```

```plaintext
tensor([[ 0.0000e+00,  1.0000e+00,  0.0000e+00,  ...,  1.0000e+00,
          0.0000e+00,  1.0000e+00],
        [ 8.4147e-01,  5.4030e-01,  8.2186e-01,  ...,  1.0000e+00,
          1.0366e-04,  1.0000e+00],
        [ 9.0930e-01, -4.1615e-01,  9.3641e-01,  ...,  1.0000e+00,
          2.0733e-04,  1.0000e+00],
        ...,
        [-6.1604e-01,  7.8771e-01,  9.3283e-01,  ...,  9.9991e-01,
          1.2958e-02,  9.9992e-01],
        [ 3.2999e-01,  9.4398e-01,  8.2756e-01,  ...,  9.9991e-01,
          1.3061e-02,  9.9991e-01],
        [ 9.7263e-01,  2.3236e-01,  1.0089e-02,  ...,  9.9991e-01,
          1.3165e-02,  9.9991e-01]])
```

```python
# 位置编码+词向量
encoder_inputs = encoder_embeddings + pe[:encoder_embeddings.size(1)]
encoder_inputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
decoder_inputs = decoder_embeddings + pe[:decoder_embeddings.size(1)]
decoder_inputs.shape
```

```plaintext
torch.Size([2, 6, 512])
```

```python
import torch
import torch.nn as nn


class MultiHeadAttention(nn.Module):

    def __init__(self, embed_dim: int, attn_dim: int, output_dim: int, num_heads: int):
        super().__init__()

        self.embed_dim = embed_dim
        self.attn_dim = attn_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.head_dim = attn_dim // num_heads  # //表示向下取整，attn_dim是head_dim的整数倍

        # QKV投影层：从输入维度映射到内部维度
        # projection
        self.q_proj = nn.Linear(embed_dim, self.attn_dim)
        self.k_proj = nn.Linear(embed_dim, self.attn_dim)
        self.v_proj = nn.Linear(embed_dim, self.attn_dim)

        # 输出投影层：从内部维度映射到输出维度
        self.out_proj = nn.Linear(self.attn_dim, self.output_dim)

    def forward(self, q_x, k_x, v_x, mask=None):
        """
        输入: [batch_size, seq_len, embed_dim]
        返回: [batch_size, seq_len, output_dim]
        """
        batch_size, q_seq_len, embed_dim = q_x.shape
        batch_size, k_seq_len, embed_dim = k_x.shape

        # 投影到QKV空间
        q = self.q_proj(q_x)  # [batch_size, seq_len, attn_dim]
        k = self.k_proj(k_x)  # [batch_size, seq_len, attn_dim]
        v = self.v_proj(v_x)  # [batch_size, seq_len, attn_dim]

        # [batch_size, seq_len, num_heads, head_dim]
        # 分割多头 [batch_size, num_heads, seq_len, head_dim]
        q = q.view(batch_size, q_seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, k_seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, k_seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # 计算注意力得分
        # q   [batch_size, num_heads, seq_len, head_dim]
        # k.T [batch_size, num_heads, head_dim, seq_len]
        # q @ k.T 形状: [batch_size, num_heads, seq_len, seq_len]
        attn_scores = torch.matmul(q, k.transpose(-2, -1))

        # 缩放因子：防止乘积过大
        d_k = k.size(-1)
        attn_scores = attn_scores / torch.sqrt(torch.tensor(d_k))

        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask == 0, float('-inf'))

        # 计算注意力权重
        attn_weights = torch.softmax(attn_scores, dim=-1)

        # 计算注意力输出
        # attn_weights [batch_size, num_heads, seq_len, seq_len]
        # v            [batch_size, num_heads, seq_len, head_dim]
        # [batch_size, num_heads, seq_len, head_dim]
        attn_out = torch.matmul(attn_weights, v)

        # 合并多头 [batch_size, seq_len, attn_dim]

        # [batch_size, seq_len, num_heads, head_dim]
        attn_out = attn_out.transpose(1, 2).reshape(batch_size, q_seq_len, self.attn_dim)

        # 投影到输出空间
        return self.out_proj(attn_out)
```

```python
## Feed Forward，两个线性层，最后输出维度不变
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))
```

```python
# 定义Encoder
class Encoder(nn.Module):
    def __init__(self, d_model, d_ff, num_heads, num_encoder_layers):
        super().__init__()
        self.layers = nn.ModuleList([EncoderLayer(d_model, d_ff, num_heads) for _ in range(num_encoder_layers)])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


# 定义EncoderLayer
class EncoderLayer(nn.Module):
    def __init__(self, d_model, d_ff, num_heads):
        super().__init__()
        self.mha = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model, num_heads=num_heads)
        self.ff = FeedForward(d_model, d_ff)
        self.layer_norm1 = nn.LayerNorm(d_model)
        self.layer_norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        # 1.多头注意力
        # 2.残差连接和层归一化
        x = self.layer_norm1(x + self.mha(q_x=x, k_x=x, v_x=x, mask=None))

        # 3.Feed Forward
        # 4.残差连接和层归一化
        return self.layer_norm2(x + self.ff(x))
```

```python
# 定义Decoder
class Decoder(nn.Module):
    def __init__(self, d_model, d_ff, num_heads, num_decoder_layers):
        super().__init__()
        self.layers = nn.ModuleList([DecoderLayer(d_model, d_ff, num_heads) for _ in range(num_decoder_layers)])

    def forward(self, decoder_inputs, encoder_outputs, mask=None):
        for layer in self.layers:
            decoder_inputs = layer(decoder_inputs, encoder_outputs, mask=mask)
        return decoder_inputs


# 定义DecoderLayer
class DecoderLayer(nn.Module):
    def __init__(self, d_model, d_ff, num_heads):
        super().__init__()
        self.masked_mha = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model,
                                             num_heads=num_heads)
        self.cross_mha = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model,
                                            num_heads=num_heads)
        self.ff = FeedForward(d_model, d_ff)
        self.layer_norm1 = nn.LayerNorm(d_model)
        self.layer_norm2 = nn.LayerNorm(d_model)
        self.layer_norm3 = nn.LayerNorm(d_model)

    def forward(self, decoder_inputs, encoder_outputs, mask=None):
        # 1.masked多头注意力
        # 2.残差连接和层归一化
        x = self.layer_norm1(
            decoder_inputs + self.masked_mha(q_x=decoder_inputs, k_x=decoder_inputs, v_x=decoder_inputs, mask=mask))

        # 3.cross多头注意力
        # 4.残差连接和层归一化
        x = self.layer_norm2(x + self.cross_mha(q_x=x, k_x=encoder_outputs, v_x=encoder_outputs))

        # 5.Feed Forward
        # 6.残差连接和层归一化
        return self.layer_norm3(x + self.ff(x))
```

```python
encoder = Encoder(d_model=d_model, d_ff=2048, num_heads=8, num_encoder_layers=6)

encoder_outputs = encoder(encoder_inputs)
encoder_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
decoder = Decoder(d_model=d_model, d_ff=2048, num_heads=8, num_decoder_layers=6)

mask = torch.tril(torch.ones(en_seq_len, en_seq_len))
decoder_outputs = decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)
decoder_outputs.shape
```

```plaintext
torch.Size([2, 6, 512])
```

```python
fc = nn.Linear(d_model, vocab_size)
decoder_outputs_vocab = fc(decoder_outputs)
decoder_outputs_vocab.shape
```

```plaintext
torch.Size([2, 6, 100])
```

```python
outputs = torch.softmax(decoder_outputs_vocab, dim=-1)
outputs.shape
```

```plaintext
torch.Size([2, 6, 100])
```

```python
class Transformer(nn.Module):
    def __init__(self, d_model, d_ff, num_heads, num_encoder_layers, num_decoder_layers):
        super().__init__()
        self.encoder = Encoder(d_model, d_ff, num_heads, num_encoder_layers)
        self.decoder = Decoder(d_model, d_ff, num_heads, num_decoder_layers)
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, encoder_inputs, decoder_inputs, mask=None):

        # 课上代码如下，有问题，用的是外面定义的，应该用self的
        # encoder_outputs = encoder(encoder_inputs)
        # decoder_outputs = decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)
        encoder_outputs = self.encoder(encoder_inputs)
        decoder_outputs = self.decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)

        return self.fc(decoder_outputs)
```

```python
transformer = Transformer(d_model=d_model, d_ff=2048, num_heads=8, num_encoder_layers=6, num_decoder_layers=6)
mask = torch.tril(torch.ones(en_seq_len, en_seq_len))
outputs = transformer(encoder_inputs, decoder_inputs, mask)
outputs.shape
```

```plaintext
torch.Size([2, 6, 100])
```

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
Building prefix dict from the default dictionary ...
Loading model from cache /var/folders/vl/mkwcfmqd5kb3rykv5bb3w3n40000gn/T/jieba.cache
Loading model cost 0.265 seconds.
Prefix dict has been built successfully.





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
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

for src, trg in dataloader:
    print(src)
    print(trg)
    break
```

```plaintext
tensor([[23, 24, 25, 26, 19,  0]])
tensor([[ 1, 20,  7, 21, 22, 23,  2,  0]])
```

```python
class Transformer(nn.Module):
    def __init__(self, d_model, d_ff, num_heads, num_encoder_layers, num_decoder_layers):
        super().__init__()
        self.encoder_embedding = nn.Embedding(vocab_size, d_model)
        self.decoder_embedding = nn.Embedding(vocab_size, d_model)
        self.encoder = Encoder(d_model, d_ff, num_heads, num_encoder_layers)
        self.decoder = Decoder(d_model, d_ff, num_heads, num_decoder_layers)
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, encoder_inputs, decoder_inputs, mask=None):
        encoder_inputs = self.encoder_embedding(encoder_inputs)
        decoder_inputs = self.decoder_embedding(decoder_inputs)

        encoder_inputs = encoder_inputs + pe[:encoder_inputs.size(1), :]
        decoder_inputs = decoder_inputs + pe[:decoder_inputs.size(1), :]

        # 课上代码如下，有问题，用的是外面定义的，应该用self的
        # encoder_outputs = encoder(encoder_inputs)
        # decoder_outputs = decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)
        encoder_outputs = self.encoder(encoder_inputs)
        decoder_outputs = self.decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)
        return self.fc(decoder_outputs)
```

```python
# transformer = Transformer(d_model=d_model, d_ff=2048, num_heads=8, num_encoder_layers=6, num_decoder_layers=6)
# optimizer = optim.Adam(transformer.parameters(), lr=0.01)

# 训练数据太少了，模型也得小一点，这样才能训练出效果，学习率也得调小一点
transformer = Transformer(d_model=d_model, d_ff=2048, num_heads=1, num_encoder_layers=2, num_decoder_layers=2)
optimizer = optim.Adam(transformer.parameters(), lr=0.0001)
criterion = nn.CrossEntropyLoss(ignore_index=en_word2idx['<pad>'])
```

```python
for epoch in range(50):
    # input： tensor([[4, 5, 6, 7, 8, 9]])
    # target：tensor([[1, 4, 5, 6, 7, 8, 9, 2]])
    for input, target in dataloader:
        # 准备解码器输入输出，其实这一步可以在数据处理时做掉
        decoder_input = target[:, :-1]  # 移除最后一个token  tensor([[1, 4, 5, 6, 7, 8, 9]])
        decoder_target = target[:, 1:]  # 移除第一个token    tensor([[4, 5, 6, 7, 8, 9, 2]])

        mask = torch.tril(torch.ones(decoder_input.size(1), decoder_input.size(1)))
        decoder_outputs = transformer(input, decoder_input, mask)

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
Epoch 1, Loss: 4.9463
Epoch 1, Loss: 4.6200
Epoch 1, Loss: 4.2976
Epoch 1, Loss: 4.2473
Epoch 1, Loss: 3.9214
Epoch 2, Loss: 2.0653
Epoch 2, Loss: 2.3686
Epoch 2, Loss: 3.0510
Epoch 2, Loss: 2.6184
Epoch 2, Loss: 2.0156
Epoch 3, Loss: 1.3953
Epoch 3, Loss: 1.7652
Epoch 3, Loss: 1.8852
Epoch 3, Loss: 1.4122
Epoch 3, Loss: 1.1573
Epoch 4, Loss: 1.1536
Epoch 4, Loss: 0.6166
Epoch 4, Loss: 0.7649
Epoch 4, Loss: 0.9722
Epoch 4, Loss: 0.4778
Epoch 5, Loss: 0.5099
Epoch 5, Loss: 0.2817
Epoch 5, Loss: 0.5702
Epoch 5, Loss: 0.3724
Epoch 5, Loss: 0.1625
Epoch 6, Loss: 0.3595
Epoch 6, Loss: 0.1484
Epoch 6, Loss: 0.1989
Epoch 6, Loss: 0.1851
Epoch 6, Loss: 0.0787
Epoch 7, Loss: 0.0692
Epoch 7, Loss: 0.1099
Epoch 7, Loss: 0.1496
Epoch 7, Loss: 0.1184
Epoch 7, Loss: 0.0792
Epoch 8, Loss: 0.0388
Epoch 8, Loss: 0.1023
Epoch 8, Loss: 0.0654
Epoch 8, Loss: 0.0814
Epoch 8, Loss: 0.0414
Epoch 9, Loss: 0.0529
Epoch 9, Loss: 0.0249
Epoch 9, Loss: 0.0334
Epoch 9, Loss: 0.0609
Epoch 9, Loss: 0.0553
Epoch 10, Loss: 0.0277
Epoch 10, Loss: 0.0513
Epoch 10, Loss: 0.0466
Epoch 10, Loss: 0.0180
Epoch 10, Loss: 0.0327
Epoch 11, Loss: 0.0393
Epoch 11, Loss: 0.0300
Epoch 11, Loss: 0.0388
Epoch 11, Loss: 0.0196
Epoch 11, Loss: 0.0149
Epoch 12, Loss: 0.0184
Epoch 12, Loss: 0.0141
Epoch 12, Loss: 0.0288
Epoch 12, Loss: 0.0233
Epoch 12, Loss: 0.0310
Epoch 13, Loss: 0.0218
Epoch 13, Loss: 0.0251
Epoch 13, Loss: 0.0152
Epoch 13, Loss: 0.0118
Epoch 13, Loss: 0.0273
Epoch 14, Loss: 0.0222
Epoch 14, Loss: 0.0111
Epoch 14, Loss: 0.0180
Epoch 14, Loss: 0.0249
Epoch 14, Loss: 0.0134
Epoch 15, Loss: 0.0168
Epoch 15, Loss: 0.0231
Epoch 15, Loss: 0.0127
Epoch 15, Loss: 0.0186
Epoch 15, Loss: 0.0097
Epoch 16, Loss: 0.0179
Epoch 16, Loss: 0.0206
Epoch 16, Loss: 0.0147
Epoch 16, Loss: 0.0117
Epoch 16, Loss: 0.0091
Epoch 17, Loss: 0.0090
Epoch 17, Loss: 0.0187
Epoch 17, Loss: 0.0110
Epoch 17, Loss: 0.0134
Epoch 17, Loss: 0.0155
Epoch 18, Loss: 0.0083
Epoch 18, Loss: 0.0128
Epoch 18, Loss: 0.0148
Epoch 18, Loss: 0.0168
Epoch 18, Loss: 0.0102
Epoch 19, Loss: 0.0101
Epoch 19, Loss: 0.0160
Epoch 19, Loss: 0.0138
Epoch 19, Loss: 0.0117
Epoch 19, Loss: 0.0075
Epoch 20, Loss: 0.0132
Epoch 20, Loss: 0.0112
Epoch 20, Loss: 0.0147
Epoch 20, Loss: 0.0072
Epoch 20, Loss: 0.0091
Epoch 21, Loss: 0.0071
Epoch 21, Loss: 0.0121
Epoch 21, Loss: 0.0104
Epoch 21, Loss: 0.0088
Epoch 21, Loss: 0.0136
Epoch 22, Loss: 0.0115
Epoch 22, Loss: 0.0066
Epoch 22, Loss: 0.0098
Epoch 22, Loss: 0.0130
Epoch 22, Loss: 0.0083
Epoch 23, Loss: 0.0082
Epoch 23, Loss: 0.0108
Epoch 23, Loss: 0.0124
Epoch 23, Loss: 0.0062
Epoch 23, Loss: 0.0092
Epoch 24, Loss: 0.0061
Epoch 24, Loss: 0.0118
Epoch 24, Loss: 0.0089
Epoch 24, Loss: 0.0076
Epoch 24, Loss: 0.0100
Epoch 25, Loss: 0.0112
Epoch 25, Loss: 0.0098
Epoch 25, Loss: 0.0073
Epoch 25, Loss: 0.0084
Epoch 25, Loss: 0.0057
Epoch 26, Loss: 0.0106
Epoch 26, Loss: 0.0081
Epoch 26, Loss: 0.0070
Epoch 26, Loss: 0.0055
Epoch 26, Loss: 0.0091
Epoch 27, Loss: 0.0100
Epoch 27, Loss: 0.0077
Epoch 27, Loss: 0.0089
Epoch 27, Loss: 0.0053
Epoch 27, Loss: 0.0066
Epoch 28, Loss: 0.0095
Epoch 28, Loss: 0.0085
Epoch 28, Loss: 0.0065
Epoch 28, Loss: 0.0073
Epoch 28, Loss: 0.0050
Epoch 29, Loss: 0.0071
Epoch 29, Loss: 0.0081
Epoch 29, Loss: 0.0049
Epoch 29, Loss: 0.0089
Epoch 29, Loss: 0.0061
Epoch 30, Loss: 0.0078
Epoch 30, Loss: 0.0087
Epoch 30, Loss: 0.0047
Epoch 30, Loss: 0.0059
Epoch 30, Loss: 0.0066
Epoch 31, Loss: 0.0066
Epoch 31, Loss: 0.0046
Epoch 31, Loss: 0.0074
Epoch 31, Loss: 0.0082
Epoch 31, Loss: 0.0057
Epoch 32, Loss: 0.0072
Epoch 32, Loss: 0.0044
Epoch 32, Loss: 0.0056
Epoch 32, Loss: 0.0061
Epoch 32, Loss: 0.0079
Epoch 33, Loss: 0.0043
Epoch 33, Loss: 0.0068
Epoch 33, Loss: 0.0060
Epoch 33, Loss: 0.0076
Epoch 33, Loss: 0.0053
Epoch 34, Loss: 0.0075
Epoch 34, Loss: 0.0041
Epoch 34, Loss: 0.0052
Epoch 34, Loss: 0.0065
Epoch 34, Loss: 0.0057
Epoch 35, Loss: 0.0050
Epoch 35, Loss: 0.0056
Epoch 35, Loss: 0.0070
Epoch 35, Loss: 0.0063
Epoch 35, Loss: 0.0039
Epoch 36, Loss: 0.0048
Epoch 36, Loss: 0.0038
Epoch 36, Loss: 0.0053
Epoch 36, Loss: 0.0061
Epoch 36, Loss: 0.0067
Epoch 37, Loss: 0.0052
Epoch 37, Loss: 0.0046
Epoch 37, Loss: 0.0059
Epoch 37, Loss: 0.0065
Epoch 37, Loss: 0.0037
Epoch 38, Loss: 0.0064
Epoch 38, Loss: 0.0050
Epoch 38, Loss: 0.0057
Epoch 38, Loss: 0.0044
Epoch 38, Loss: 0.0036
Epoch 39, Loss: 0.0048
Epoch 39, Loss: 0.0044
Epoch 39, Loss: 0.0035
Epoch 39, Loss: 0.0055
Epoch 39, Loss: 0.0060
Epoch 40, Loss: 0.0042
Epoch 40, Loss: 0.0046
Epoch 40, Loss: 0.0053
Epoch 40, Loss: 0.0034
Epoch 40, Loss: 0.0058
Epoch 41, Loss: 0.0045
Epoch 41, Loss: 0.0033
Epoch 41, Loss: 0.0057
Epoch 41, Loss: 0.0051
Epoch 41, Loss: 0.0040
Epoch 42, Loss: 0.0044
Epoch 42, Loss: 0.0050
Epoch 42, Loss: 0.0055
Epoch 42, Loss: 0.0039
Epoch 42, Loss: 0.0031
Epoch 43, Loss: 0.0031
Epoch 43, Loss: 0.0042
Epoch 43, Loss: 0.0038
Epoch 43, Loss: 0.0053
Epoch 43, Loss: 0.0048
Epoch 44, Loss: 0.0038
Epoch 44, Loss: 0.0041
Epoch 44, Loss: 0.0051
Epoch 44, Loss: 0.0030
Epoch 44, Loss: 0.0046
Epoch 45, Loss: 0.0040
Epoch 45, Loss: 0.0046
Epoch 45, Loss: 0.0036
Epoch 45, Loss: 0.0050
Epoch 45, Loss: 0.0029
Epoch 46, Loss: 0.0029
Epoch 46, Loss: 0.0035
Epoch 46, Loss: 0.0048
Epoch 46, Loss: 0.0044
Epoch 46, Loss: 0.0038
Epoch 47, Loss: 0.0043
Epoch 47, Loss: 0.0028
Epoch 47, Loss: 0.0047
Epoch 47, Loss: 0.0038
Epoch 47, Loss: 0.0034
Epoch 48, Loss: 0.0034
Epoch 48, Loss: 0.0037
Epoch 48, Loss: 0.0027
Epoch 48, Loss: 0.0045
Epoch 48, Loss: 0.0041
Epoch 49, Loss: 0.0033
Epoch 49, Loss: 0.0044
Epoch 49, Loss: 0.0026
Epoch 49, Loss: 0.0040
Epoch 49, Loss: 0.0035
Epoch 50, Loss: 0.0040
Epoch 50, Loss: 0.0043
Epoch 50, Loss: 0.0026
Epoch 50, Loss: 0.0035
Epoch 50, Loss: 0.0031
```

```python
# 翻译函数

def translate(sentence, transformer):

    zh_tokens = torch.LongTensor(tokenize(chinese_split(sentence), zh_word2idx))

    zh_embeddings = transformer.encoder_embedding(zh_tokens).unsqueeze(0)
    zh_embeddings = zh_embeddings + pe[:zh_embeddings.size(1), :]
    encoder_outputs = transformer.encoder(zh_embeddings)

    decoder_inputs = [en_word2idx['<bos>']]

    for _ in range(50):
        with torch.no_grad():
            decoder_inputs_tensor = torch.LongTensor(decoder_inputs)
            decoder_inputs_tensor = transformer.decoder_embedding(decoder_inputs_tensor).unsqueeze(0)
            decoder_inputs_tensor = decoder_inputs_tensor + pe[:decoder_inputs_tensor.size(1), :]

            output = transformer.decoder(decoder_inputs=decoder_inputs_tensor, encoder_outputs=encoder_outputs, mask=None)
            output = transformer.fc(output)
            pred_token = output[:,-1,:].argmax().item()
            decoder_inputs.append(pred_token)

            if pred_token == en_word2idx['<eos>']:
                break

    return ' '.join([en_vocab[idx] for idx in decoder_inputs[1:-1]])


# 测试翻译
test_sentence = "我们一起学习"
print(translate(test_sentence, transformer))
```

```plaintext
let's study together.
```