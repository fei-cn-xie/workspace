# 44、手写DeepSeek之GQA、MQA、MLA

MHA、GQA、MQA、MLA

DeepSeek-LLM模型中用的是GQA，也就是grouped-query attention，GQA表示分组查询注意力机制。

DeepSeek V2、V3用的是MLA，也就是Multi-head Latent Attention，也就是多头潜在注意力机制。
DeepSeek R1是基于V3通过强化学习训练出来的，所以也是用的MLA。

GQA论文：https://arxiv.org/abs/2305.13245

```python
import torch

# x表示一个输入的seq，有4个词，每个词向量长度为8
x = torch.rand(4, 8)

# w是二维矩阵
wq_head1 = torch.rand(8, 8)
wq_head2 = torch.rand(8, 8)
wq_head3 = torch.rand(8, 8)
wq_head4 = torch.rand(8, 8)

wk_group1 = torch.rand(8, 8)
wk_group2 = torch.rand(8, 8)

wv_group1 = torch.rand(8, 8)
wv_group2 = torch.rand(8, 8)

q_head1 = torch.matmul(x, wq_head1)
q_head2 = torch.matmul(x, wq_head2)
q_head3 = torch.matmul(x, wq_head3)
q_head4 = torch.matmul(x, wq_head4)

k_group1 = torch.matmul(x, wk_group1) # 第1个Q和第2个Q对应第1组，第3个Q和第4个Q对应第2组
k_group2 = torch.matmul(x, wk_group2)

v_group1 = torch.matmul(x, wv_group1)
v_group2 = torch.matmul(x, wv_group2)
```

```python
qk_score_head1 = torch.matmul(q_head1, k_group1.T)
dk_head1 = k_group1.size(-1)
qk_weight_head1 = torch.softmax(qk_score_head1 / torch.sqrt(torch.tensor(dk_head1)), dim=-1)
o_head1 = torch.matmul(qk_weight_head1, v_group1)
```

```python
qk_score_head2 = torch.matmul(q_head2, k_group1.T)
dk_head2 = k_group1.size(-1)
qk_weight_head2 = torch.softmax(qk_score_head2 / torch.sqrt(torch.tensor(dk_head2)), dim=-1)
o_head2 = torch.matmul(qk_weight_head2, v_group1)
```

```python
qk_score_head3 = torch.matmul(q_head3, k_group2.T)
dk_head3 = k_group2.size(-1)
qk_weight_head3 = torch.softmax(qk_score_head3 / torch.sqrt(torch.tensor(dk_head3)), dim=-1)
o_head3 = torch.matmul(qk_weight_head3, v_group2)
```

```python
qk_score_head4 = torch.matmul(q_head4, k_group2.T)
dk_head4 = k_group2.size(-1)
qk_weight_head4 = torch.softmax(qk_score_head4 / torch.sqrt(torch.tensor(dk_head4)), dim=-1)
o_head4 = torch.matmul(qk_weight_head4, v_group2)
```

```python
o = torch.cat([o_head1, o_head2, o_head3, o_head4], dim=1)
o
```

```plaintext
tensor([[2.4892, 2.2409, 3.0830, 1.9829, 1.3328, 1.7617, 2.1029, 2.2179, 2.5397,
         2.2371, 3.0668, 1.9731, 1.3336, 1.7150, 2.1268, 2.2563, 1.7857, 2.2017,
         2.5348, 1.9395, 2.0288, 2.7907, 2.6411, 2.9243, 1.7816, 2.1895, 2.4880,
         1.8965, 2.0238, 2.7434, 2.6256, 2.9122],
        [2.5552, 2.2504, 3.1093, 1.9817, 1.3569, 1.7436, 2.1377, 2.2815, 2.5890,
         2.2504, 3.1021, 1.9783, 1.3595, 1.7155, 2.1530, 2.3079, 1.7906, 2.2065,
         2.5828, 1.9795, 2.0201, 2.8361, 2.6535, 2.9298, 1.7834, 2.2026, 2.5204,
         1.9290, 2.0361, 2.7784, 2.6378, 2.9247],
        [2.5334, 2.2508, 3.1048, 1.9868, 1.3515, 1.7533, 2.1251, 2.2612, 2.6769,
         2.2639, 3.1331, 1.9789, 1.3901, 1.6876, 2.1978, 2.3910, 1.7895, 2.2071,
         2.5700, 1.9696, 2.0252, 2.8246, 2.6513, 2.9300, 1.7861, 2.2060, 2.5471,
         1.9517, 2.0326, 2.8040, 2.6451, 2.9284],
        [2.4949, 2.2395, 3.0766, 1.9814, 1.3308, 1.7523, 2.1050, 2.2209, 2.5820,
         2.2445, 3.0913, 1.9724, 1.3524, 1.7103, 2.1503, 2.2993, 1.7857, 2.1968,
         2.5180, 1.9231, 2.0244, 2.7729, 2.6365, 2.9196, 1.7820, 2.1948, 2.4871,
         1.8982, 2.0324, 2.7443, 2.6286, 2.9171]])
```

```python
wo = torch.rand(4*8, 8)
out_put = torch.matmul(o, wo)
out_put
```

```plaintext
tensor([[35.3237, 32.7969, 37.6285, 39.0346, 41.6376, 33.9676, 38.3575, 40.0775],
        [35.6853, 33.1366, 38.0081, 39.4083, 42.0654, 34.2874, 38.7489, 40.4958],
        [35.7997, 33.3191, 38.1082, 39.5443, 42.1714, 34.4032, 38.9020, 40.6494],
        [35.3413, 32.8691, 37.6597, 39.0699, 41.6656, 34.0233, 38.4128, 40.1341]])
```

多头注意力就是增加了另外的q、k、v，从而可以从多个角度来捕捉token之间的相关性。

```python
import torch
import torch.nn as nn


class GQAAttention(nn.Module):

    def __init__(self, embed_dim: int, attn_dim: int, output_dim: int, num_heads: int, num_kv_groups: int):
        super().__init__()

        self.embed_dim = embed_dim
        self.attn_dim = attn_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.num_kv_groups = num_kv_groups  # 新增
        self.head_dim = attn_dim // num_heads

        # QKV投影层：从输入维度映射到内部维度
        self.q_proj = nn.Linear(embed_dim, self.attn_dim)

        self.kv_attn_dim = self.head_dim * self.num_kv_groups
        self.k_proj = nn.Linear(embed_dim, self.kv_attn_dim)
        self.v_proj = nn.Linear(embed_dim, self.kv_attn_dim)

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
        k = self.k_proj(x)  # [batch_size, seq_len, kv_attn_dim]
        v = self.v_proj(x)  # [batch_size, seq_len, kv_attn_dim]

        # [batch_size, seq_len, num_heads, head_dim]
        # 分割多头 [batch_size, num_heads, seq_len, head_dim]
        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        k = k.view(batch_size, seq_len, self.num_kv_groups, self.head_dim).transpose(1, 2)

        v = v.view(batch_size, seq_len, self.num_kv_groups, self.head_dim).transpose(1, 2)

        rep_factor = self.num_heads // self.num_kv_groups
        k = k.repeat_interleave(rep_factor, dim=1)
        v = v.repeat_interleave(rep_factor, dim=1)

        if kv_cache is not None:
            # 获取缓存的kv
            k_cache, v_cache = kv_cache
            # 拼接缓存的kv和当前的kv
            k = torch.cat([k_cache, k], dim=2)
            v = torch.cat([v_cache, v], dim=2)
            # 更新缓存的kv
            kv_cache = (k, v)
        else:
            kv_cache = (k, v)

        # 计算注意力得分
        # q   [batch_size, num_heads, seq_len, head_dim]
        # k.T [batch_size, num_heads, head_dim, seq_len]
        # q @ k.T 形状: [batch_size, num_heads, seq_len, seq_len]
        # 1,4,4,2
        # 1,4,2,4
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
x = torch.rand(1, 4, 2)

attn = GQAAttention(embed_dim=2, attn_dim=8, output_dim=8, num_heads=4, num_kv_groups=2)
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

```python
import torch

batch_size = 1
seq_len = 1
num_heads = 4
head_dim = 1
num_kv_headers = 2

# 测试repeat函数效果
q = torch.rand(batch_size, num_heads, seq_len, head_dim)
print(q)

k = torch.rand(batch_size, num_kv_headers, seq_len, head_dim)
print(k)

rep_factor = num_heads // num_kv_headers
k_repeated = k.repeat_interleave(rep_factor, dim=1)
print(k_repeated)

attn_scores = torch.matmul(q, k_repeated.transpose(-2, -1))
print(attn_scores.shape)
```

```plaintext
tensor([[[[0.4041]],

         [[0.6990]],

         [[0.2889]],

         [[0.5308]]]])
tensor([[[[0.4436]],

         [[0.8200]]]])
tensor([[[[0.4436]],

         [[0.4436]],

         [[0.8200]],

         [[0.8200]]]])
torch.Size([1, 4, 1, 1])
```