# 43、手写DeepSeek之KV Cache

## KV Cache

只用在推理过程中。

“我是”-->“周”

“我是周”--->“瑜”

“我是周瑜”--->“...”

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
        self.head_dim = attn_dim // num_heads # //表示向下取整，attn_dim是head_dim的整数倍

        # QKV投影层：从输入维度映射到内部维度
        # projection
        self.q_proj = nn.Linear(embed_dim, self.attn_dim)
        self.k_proj = nn.Linear(embed_dim, self.attn_dim)
        self.v_proj = nn.Linear(embed_dim, self.attn_dim)

        # 输出投影层：从内部维度映射到输出维度
        self.out_proj = nn.Linear(self.attn_dim, self.output_dim)

    def forward(self, x, kv_cache=None):
        """
        输入: [batch_size, seq_len, embed_dim]
        返回: [batch_size, seq_len, output_dim]
        """
        batch_size, seq_len, embed_dim = x.shape

        # 投影到QKV空间
        q = self.q_proj(x)  # [batch_size, seq_len, attn_dim]
        k = self.k_proj(x)  # [batch_size, seq_len, attn_dim]
        v = self.v_proj(x)  # [batch_size, seq_len, attn_dim]

        # [batch_size, seq_len, num_heads, head_dim]
        # 分割多头 [batch_size, num_heads, seq_len, head_dim]
        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        if kv_cache is not None:
            # 获取缓存的kv
            k_cache, v_cache = kv_cache
            # 拼接缓存的kv和当前的kv
            k = torch.cat([k_cache, k], dim=2)  # 256, 128 --> cache ---> 128, 256  MLA
            v = torch.cat([v_cache, v], dim=2)
            # 更新缓存的kv
            kv_cache = (k, v)
        else:
            kv_cache = (k, v)

        # 计算注意力得分
        # q   [batch_size, num_heads, seq_len, head_dim]
        # k.T [batch_size, num_heads, head_dim, seq_len]
        # q @ k.T 形状: [batch_size, num_heads, seq_len, seq_len]
        attn_scores = torch.matmul(q, k.transpose(-2, -1))

        # 缩放因子：防止乘积过大
        d_k = k.size(-1)
        attn_scores = attn_scores / torch.sqrt(torch.tensor(d_k))

        # 计算注意力权重
        attn_weights = torch.softmax(attn_scores, dim=-1)

        # 计算注意力输出
        # attn_weights [batch_size, num_heads, seq_len, seq_len]
        # v            [batch_size, num_heads, seq_len, head_dim]
        # [batch_size, num_heads, seq_len, head_dim]
        attn_out = torch.matmul(attn_weights, v)

        # 合并多头 [batch_size, seq_len, attn_dim]

        # [batch_size, seq_len, num_heads, head_dim]
        attn_out = attn_out.transpose(1, 2).reshape(batch_size, seq_len, self.attn_dim)

        # 投影到输出空间
        return self.out_proj(attn_out), kv_cache
```

```python
# 一个seq
x = torch.rand(1, 4, 2)

attn = MultiHeadAttention(embed_dim=2, attn_dim=6, output_dim=8, num_heads=2)
out, kv_cache = attn(x)

print(x.shape)
print(out.shape)

x = torch.rand(1, 5, 2)
out, kv_cache = attn(x[:, -1:, :], kv_cache)
print(x.shape)
print(out.shape)
```

```plaintext
torch.Size([1, 4, 2])
torch.Size([1, 4, 8])
torch.Size([1, 5, 2])
torch.Size([1, 1, 8])
```