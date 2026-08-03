# 28、手写Transformer中Decoder实现

```python
import torch
import torch.nn as nn

batch_size = 2
seq_len = 5
d_model = 512  # 词向量的长度
vocab_size = 100

# 生成两个句子，每个句子有5个词
# 随机生成0-100的数字，形状为(batch_size, seq_len)，表示batch_size条sequence，每条sequence的长度为seq_len
inputs = torch.randint(0, vocab_size, (batch_size, seq_len))
inputs
```

```plaintext
tensor([[61, 81, 31, 40, 17],
        [ 4, 95, 48, 24, 12]])
```

```python
# 词嵌入层
# 两个句子，每个句子有5个词，每个词的词向量长度为512
embedding = nn.Embedding(vocab_size, d_model)
embeddings = embedding(inputs)
embeddings.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
import math

# 位置编码
# 位置编码只跟位置有关，和具体位置上输入的数据无关
pe = torch.zeros(seq_len, d_model)
position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
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
        [ 1.4112e-01, -9.8999e-01,  2.4509e-01,  ...,  1.0000e+00,
          3.1099e-04,  1.0000e+00],
        [-7.5680e-01, -6.5364e-01, -6.5717e-01,  ...,  1.0000e+00,
          4.1465e-04,  1.0000e+00]])
```

```python
# 位置编码+词向量
decoder_inputs = embeddings + pe
decoder_inputs.shape
```

```plaintext
torch.Size([2, 5, 512])
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
attn = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model, num_heads=2)

mask = torch.tril(torch.ones(seq_len, seq_len))

decoder_mask_attn_outputs = attn(q_x=decoder_inputs, k_x=decoder_inputs, v_x=decoder_inputs, mask=mask)

print(decoder_inputs.shape)
print(decoder_mask_attn_outputs.shape)
```

```plaintext
torch.Size([2, 5, 512])
torch.Size([2, 5, 512])
```

```python
## 残差连接
decoder_mask_attn_add_outputs = decoder_inputs + decoder_mask_attn_outputs
decoder_mask_attn_add_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
## 层归一化
layer_norm_1 = nn.LayerNorm(d_model)
decoder_mask_attn_add_norm_outputs = layer_norm_1(decoder_mask_attn_add_outputs)
decoder_mask_attn_add_norm_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
# 模拟Encoder的输出（2, 4, 512）
encoder_outputs = torch.randn(batch_size, 4, d_model)

cross_attn = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model, num_heads=2)
decoder_mask_attn_add_norm_cross_outputs = cross_attn(q_x=decoder_mask_attn_add_norm_outputs, k_x=encoder_outputs,
                                                      v_x=encoder_outputs, mask=None)
```

```python
## 残差连接
decoder_mask_attn_add_norm_cross_add_outputs = decoder_mask_attn_add_norm_outputs + decoder_mask_attn_add_norm_cross_outputs

## 层归一化
layer_norm_2 = nn.LayerNorm(d_model)
decoder_mask_attn_add_norm_cross_add_norm_outputs = layer_norm_2(decoder_mask_attn_add_norm_cross_add_outputs)
decoder_mask_attn_add_norm_cross_add_norm_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
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


feed_forward = FeedForward(d_model=d_model, d_ff=2048)

decoder_mask_attn_add_norm_cross_add_norm_feed_outputs = feed_forward(decoder_mask_attn_add_norm_cross_add_norm_outputs)
decoder_mask_attn_add_norm_cross_add_norm_feed_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
# 再来一次残差连接和层归一化，得到最终的Encoder输出
layer_norm_3 = nn.LayerNorm(d_model)
decoder_outputs = layer_norm_3(
    decoder_mask_attn_add_norm_cross_add_norm_feed_outputs + decoder_mask_attn_add_norm_cross_add_norm_outputs)
decoder_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
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
        x = self.layer_norm1(decoder_inputs + self.masked_mha(q_x=decoder_inputs, k_x=decoder_inputs, v_x=decoder_inputs, mask=mask))

        # 3.cross多头注意力
        # 4.残差连接和层归一化
        x = self.layer_norm2(x + self.cross_mha(q_x=x, k_x=encoder_outputs, v_x=encoder_outputs))

        # 5.Feed Forward
        # 6.残差连接和层归一化
        return self.layer_norm3(x + self.ff(x))


decoder = Decoder(d_model=512, d_ff=2048, num_heads=8, num_decoder_layers=6)

mask = torch.tril(torch.ones(seq_len, seq_len))
decoder_outputs = decoder(decoder_inputs=decoder_inputs, encoder_outputs=encoder_outputs, mask=mask)
decoder_outputs.shape
```

```plaintext
torch.Size([2, 5, 512])
```

```python
fc = nn.Linear(d_model, vocab_size)
decoder_outputs_vocab = fc(decoder_outputs)
decoder_outputs_vocab.shape
```

```plaintext
torch.Size([2, 5, 100])
```

```python
outputs = torch.softmax(decoder_outputs_vocab, dim=-1)
outputs.shape
```

```plaintext
torch.Size([2, 5, 100])
```