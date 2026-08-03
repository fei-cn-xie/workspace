# 32、手写BERT以及预训练BERT

## BERT

BERT模型全称是Bidirectional encoder representations from transformers (BERT)，基于Transformer的双向编码器模型，重点是只用了Transformer中的编码器。

BERT为了理解文本，做了两件事，一件是MLM，既Mask Language Model，就是将输入的文本中某些词进行Mask，然后训练模型，使得模型能正确预测被Mask的词，也就是完形填空。

第二件事是NSP，既下一句预测，判断一个句子是不是另一个句子的下一句，NSP是一个二分类任务，它给定两个输入句子 [CLS] A [SEP] B [SEP]，模型只需要输出一个二分类预测：B 是不是 A 的下一个句子（是/否），和GPT不同，GPT是预测新的文本。

```python
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


## Feed Forward，两个线性层，最后输出维度不变
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


# 定义Encoder
class Encoder(nn.Module):
    def __init__(self, d_model, d_ff, num_heads, num_encoder_layers):
        super().__init__()
        self.layers = nn.ModuleList([EncoderLayer(d_model, d_ff, num_heads) for _ in range(num_encoder_layers)])

    def forward(self, x, mask):
        for layer in self.layers:
            x = layer(x, mask)
        return x


# 定义EncoderLayer
class EncoderLayer(nn.Module):
    def __init__(self, d_model, d_ff, num_heads):
        super().__init__()
        self.mha = MultiHeadAttention(embed_dim=d_model, attn_dim=d_model, output_dim=d_model, num_heads=num_heads)
        self.ff = FeedForward(d_model, d_ff)
        self.layer_norm1 = nn.LayerNorm(d_model)
        self.layer_norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask):
        # 1.多头注意力
        # 2.残差连接和层归一化
        x = self.layer_norm1(x + self.mha(q_x=x, k_x=x, v_x=x, mask=mask))

        # 3.Feed Forward
        # 4.残差连接和层归一化
        return self.layer_norm2(x + self.ff(x))
```

```python
# BERT模型
d_model = 64
d_ff = d_model * 2
num_heads = 2
num_encoder_layers = 2


class BERTModel(nn.Module):
    def __init__(self, vocab_size, max_seq_len):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Embedding(max_seq_len, d_model)
        self.segment_embedding = nn.Embedding(2, d_model)
        self.encoder = Encoder(d_model, d_ff, num_heads, num_encoder_layers)

        # MLM输出层
        self.mlm_head = nn.Sequential(
            nn.Linear(d_model, vocab_size)
        )

        # NSP输出层
        self.nsp_head = nn.Sequential(
            nn.Linear(d_model, 2)  # 二分类输出
        )

    def forward(self, input_ids, segment_ids, attention_mask):
        batch_size, seq_len = input_ids.shape

        # src_ids表示词在词汇表中的索引
        token_embeddings = self.token_embedding(input_ids)

        # pos_ids表示词在seq_len中的位置
        pos_ids = torch.arange(0, seq_len).unsqueeze(0).repeat(batch_size, 1)
        pos_embeddings = self.pos_embedding(pos_ids)

        # segment_embeddings表示词对应的segment的索引
        segment_embeddings = self.segment_embedding(segment_ids)

        embeddings = token_embeddings + pos_embeddings + segment_embeddings

        encoder_output = self.encoder(embeddings, attention_mask)

        # 获取CLS位置表示用于NSP
        cls_output = encoder_output[:, 0, :]

        # MLM和NSP输出
        nsp_output = self.nsp_head(cls_output)
        mlm_output = self.mlm_head(encoder_output)


        return mlm_output, nsp_output
```

独立寒秋
湘江北去
橘子洲头

seq [CLS]独立寒秋[SEP]湘江北去[SEP] 1
seq [CLS]独立寒秋[SEP]橘子洲头[SEP] 0

[CLS]独立寒秋[SEP]湘江北去[SEP]

[CLS]独[MASK]寒秋[SEP]湘江北去[SEP] NSP 1
MLM 立

```python
from collections import Counter
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# 示例文本数据，一首诗
data = """
独立寒秋，湘江北去，橘子洲头。
看万山红遍，层林尽染；漫江碧透，百舸争流。
鹰击长空，鱼翔浅底，万类霜天竞自由。
怅寥廓，问苍茫大地，谁主沉浮？
携来百侣曾游，忆往昔峥嵘岁月稠。
恰同学少年，风华正茂；书生意气，挥斥方遒。
指点江山，激扬文字，粪土当年万户侯。
曾记否，到中流击水，浪遏飞舟？
"""

# 处理特殊符号
special_tokens = ['[PAD]', '[UNK]', '[SEP]', '[CLS]', '[MASK]']


# 构建词汇表
def build_vocab(text):
    counter = Counter()

    for word in text:
        counter[word] += 1

    vocab = special_tokens.copy()

    for word, count in counter.items():
        if word not in special_tokens:
            vocab.append(word)

    word2idx = {word: idx for idx, word in enumerate(vocab)}
    return vocab, word2idx


# 构建中英文词汇表
vocab, word2idx = build_vocab(data)
id2word = {idx: word for word, idx in word2idx.items()}

print(word2idx)
```

```plaintext
{'[PAD]': 0, '[UNK]': 1, '[SEP]': 2, '[CLS]': 3, '[MASK]': 4, '\n': 5, '独': 6, '立': 7, '寒': 8, '秋': 9, '，': 10, '湘': 11, '江': 12, '北': 13, '去': 14, '橘': 15, '子': 16, '洲': 17, '头': 18, '。': 19, '看': 20, '万': 21, '山': 22, '红': 23, '遍': 24, '层': 25, '林': 26, '尽': 27, '染': 28, '；': 29, '漫': 30, '碧': 31, '透': 32, '百': 33, '舸': 34, '争': 35, '流': 36, '鹰': 37, '击': 38, '长': 39, '空': 40, '鱼': 41, '翔': 42, '浅': 43, '底': 44, '类': 45, '霜': 46, '天': 47, '竞': 48, '自': 49, '由': 50, '怅': 51, '寥': 52, '廓': 53, '问': 54, '苍': 55, '茫': 56, '大': 57, '地': 58, '谁': 59, '主': 60, '沉': 61, '浮': 62, '？': 63, '携': 64, '来': 65, '侣': 66, '曾': 67, '游': 68, '忆': 69, '往': 70, '昔': 71, '峥': 72, '嵘': 73, '岁': 74, '月': 75, '稠': 76, '恰': 77, '同': 78, '学': 79, '少': 80, '年': 81, '风': 82, '华': 83, '正': 84, '茂': 85, '书': 86, '生': 87, '意': 88, '气': 89, '挥': 90, '斥': 91, '方': 92, '遒': 93, '指': 94, '点': 95, '激': 96, '扬': 97, '文': 98, '字': 99, '粪': 100, '土': 101, '当': 102, '户': 103, '侯': 104, '记': 105, '否': 106, '到': 107, '中': 108, '水': 109, '浪': 110, '遏': 111, '飞': 112, '舟': 113}
```

```python
import random

# 超参数设置
MAX_SEQ_LENGTH = 20
BATCH_SIZE = 1
MASK_RATE = 0.15  # MLM掩码比例


# 创建训练数据
class ZhouyuBertDataset(Dataset):
    def __init__(self, data, max_seq_length=20):
        self.data = [ch for ch in data if ch not in ('\n', '，', '？', '。')]
        self.max_seq_length = max_seq_length
        # 4个词一个句子
        self.sentences = [self.data[i:i + 4] for i in range(0, len(self.data), 4)]
        print(f"句子数量: {len(self.sentences)}")
        print(self.sentences)

    def __len__(self):
        return len(self.sentences) // 2

    def __getitem__(self, idx):  # 2 di
        # 改进NSP任务的平衡性
        is_next = random.random() > 0.5  # 50%正样本，50%负样本

        # 获取句子A
        a_idx = idx * 2
        sentence_a = list(self.sentences[a_idx])

        # 获取句子B
        if is_next and a_idx + 1 < len(self.sentences):
            sentence_b = list(self.sentences[a_idx + 1])
        else:
            # 随机选择非相邻句子
            b_idx = random.randint(0, len(self.sentences) - 1)
            while abs(b_idx - a_idx) <= 1:
                b_idx = random.randint(0, len(self.sentences) - 1)
            sentence_b = list(self.sentences[b_idx])
            is_next = False

        # 创建输入序列
        tokens = ['[CLS]'] + sentence_a + ['[SEP]'] + sentence_b + ['[SEP]']

        # 截断或填充
        if len(tokens) > self.max_seq_length:
            tokens = tokens[:self.max_seq_length - 1] + ['[SEP]']
        elif len(tokens) < self.max_seq_length:
            tokens += ['[PAD]'] * (self.max_seq_length - len(tokens))

        # 转换为ID
        input_ids = [word2idx.get(token, word2idx['[UNK]']) for token in tokens]

        # 创建segment ID
        sep_positions = [i for i, token in enumerate(tokens) if token == '[SEP]']
        segment_ids = [0] * self.max_seq_length
        if len(sep_positions) >= 2:
            for i in range(sep_positions[0] + 1, sep_positions[1] + 1):
                segment_ids[i] = 1

        # attention mask
        attention_mask = [1 if token != '[PAD]' else 0 for token in tokens]

        # MLM标签
        mlm_labels = [-100] * self.max_seq_length

        # 掩码策略
        maskable_positions = []
        for i, token in enumerate(tokens):
            if token not in ['[CLS]', '[SEP]', '[PAD]']:
                maskable_positions.append(i)

        # 随机选择15%的位置进行掩码
        num_mask = max(1, int(len(maskable_positions) * 0.15))
        mask_positions = random.sample(maskable_positions, min(num_mask, len(maskable_positions)))

        for i in mask_positions:
            mlm_labels[i] = input_ids[i]  # 保存原始ID

            rand = random.random()
            if rand < 0.8:  # 80%替换为[MASK]
                input_ids[i] = word2idx['[MASK]']
            elif rand < 0.9:  # 10%随机替换
                available_tokens = [idx for idx in range(len(vocab))
                                    if idx not in [word2idx['[CLS]'], word2idx['[SEP]'],
                                                   word2idx['[PAD]'], word2idx['[MASK]']]]
                if available_tokens:
                    input_ids[i] = random.choice(available_tokens)
            # 10%保持不变

        return {
            'input_ids': torch.LongTensor(input_ids),
            'segment_ids': torch.LongTensor(segment_ids),
            'attention_mask': torch.LongTensor(attention_mask),
            'mlm_labels': torch.LongTensor(mlm_labels),
            'nsp_label': torch.LongTensor([int(is_next)])
        }



dataset = ZhouyuBertDataset(data)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

for result in dataloader:
    print(result)
    break
```

```plaintext
句子数量: 29
[['独', '立', '寒', '秋'], ['湘', '江', '北', '去'], ['橘', '子', '洲', '头'], ['看', '万', '山', '红'], ['遍', '层', '林', '尽'], ['染', '；', '漫', '江'], ['碧', '透', '百', '舸'], ['争', '流', '鹰', '击'], ['长', '空', '鱼', '翔'], ['浅', '底', '万', '类'], ['霜', '天', '竞', '自'], ['由', '怅', '寥', '廓'], ['问', '苍', '茫', '大'], ['地', '谁', '主', '沉'], ['浮', '携', '来', '百'], ['侣', '曾', '游', '忆'], ['往', '昔', '峥', '嵘'], ['岁', '月', '稠', '恰'], ['同', '学', '少', '年'], ['风', '华', '正', '茂'], ['；', '书', '生', '意'], ['气', '挥', '斥', '方'], ['遒', '指', '点', '江'], ['山', '激', '扬', '文'], ['字', '粪', '土', '当'], ['年', '万', '户', '侯'], ['曾', '记', '否', '到'], ['中', '流', '击', '水'], ['浪', '遏', '飞', '舟']]
{'input_ids': tensor([[  3,  29,  86, 107,  88,   2,  66,  67,  68,  69,   2,   0,   0,   0,
           0,   0,   0,   0,   0,   0]]), 'segment_ids': tensor([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'mlm_labels': tensor([[-100, -100, -100,   87, -100, -100, -100, -100, -100, -100, -100, -100,
         -100, -100, -100, -100, -100, -100, -100, -100]]), 'nsp_label': tensor([[0]])}
```

```python
model = BERTModel(len(vocab), MAX_SEQ_LENGTH)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

mlm_criterion = nn.CrossEntropyLoss(ignore_index=-100)
nsp_criterion = nn.CrossEntropyLoss()

# 训练循环
for epoch in range(200):
    for batch in dataloader:
        input_ids = batch['input_ids']
        segment_ids = batch['segment_ids']
        attention_mask = batch['attention_mask']
        mlm_labels = batch['mlm_labels']
        nsp_labels = batch['nsp_label'].squeeze(1)

        mlm_output, nsp_output = model(input_ids, segment_ids, attention_mask)
        mlm_loss = mlm_criterion(mlm_output.view(-1, mlm_output.size(-1)), mlm_labels.view(-1))
        nsp_loss = nsp_criterion(nsp_output, nsp_labels)
        loss = mlm_loss + nsp_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch {epoch + 1}, Loss: {loss:.4f}, MLM Loss: {mlm_loss:.4f}, NSP Loss: {nsp_loss:.4f}')
```

```plaintext
Epoch 1, Loss: 5.5818, MLM Loss: 4.7740, NSP Loss: 0.8078
Epoch 1, Loss: 4.7456, MLM Loss: 4.3268, NSP Loss: 0.4188
Epoch 1, Loss: 6.0570, MLM Loss: 4.3775, NSP Loss: 1.6795
Epoch 1, Loss: 5.3308, MLM Loss: 5.1620, NSP Loss: 0.1688
Epoch 1, Loss: 7.2129, MLM Loss: 5.6064, NSP Loss: 1.6064
Epoch 1, Loss: 5.1323, MLM Loss: 4.8789, NSP Loss: 0.2534
Epoch 1, Loss: 6.0922, MLM Loss: 4.7616, NSP Loss: 1.3306
Epoch 1, Loss: 6.1420, MLM Loss: 5.7749, NSP Loss: 0.3671
Epoch 1, Loss: 4.5531, MLM Loss: 4.1439, NSP Loss: 0.4092
Epoch 1, Loss: 6.2906, MLM Loss: 5.8668, NSP Loss: 0.4238
Epoch 1, Loss: 4.9923, MLM Loss: 4.6141, NSP Loss: 0.3781
Epoch 1, Loss: 6.3126, MLM Loss: 5.0225, NSP Loss: 1.2902
Epoch 1, Loss: 4.8964, MLM Loss: 3.7787, NSP Loss: 1.1177
Epoch 1, Loss: 5.6252, MLM Loss: 5.1929, NSP Loss: 0.4323
Epoch 11, Loss: 5.5907, MLM Loss: 4.8009, NSP Loss: 0.7898
Epoch 11, Loss: 4.8473, MLM Loss: 4.3391, NSP Loss: 0.5082
Epoch 11, Loss: 6.9851, MLM Loss: 6.1433, NSP Loss: 0.8418
Epoch 11, Loss: 6.0997, MLM Loss: 5.3619, NSP Loss: 0.7379
Epoch 11, Loss: 3.9591, MLM Loss: 3.3933, NSP Loss: 0.5657
Epoch 11, Loss: 4.9064, MLM Loss: 4.4728, NSP Loss: 0.4336
Epoch 11, Loss: 6.5616, MLM Loss: 5.5392, NSP Loss: 1.0224
Epoch 11, Loss: 5.4201, MLM Loss: 4.3985, NSP Loss: 1.0216
Epoch 11, Loss: 5.4150, MLM Loss: 4.3246, NSP Loss: 1.0904
Epoch 11, Loss: 4.5733, MLM Loss: 4.0385, NSP Loss: 0.5347
Epoch 11, Loss: 4.5058, MLM Loss: 4.0250, NSP Loss: 0.4809
Epoch 11, Loss: 3.3730, MLM Loss: 2.9273, NSP Loss: 0.4457
Epoch 11, Loss: 4.5096, MLM Loss: 3.4748, NSP Loss: 1.0349
Epoch 11, Loss: 5.3701, MLM Loss: 4.4023, NSP Loss: 0.9677
Epoch 21, Loss: 5.9648, MLM Loss: 5.6378, NSP Loss: 0.3270
Epoch 21, Loss: 6.5650, MLM Loss: 6.1065, NSP Loss: 0.4584
Epoch 21, Loss: 6.8936, MLM Loss: 6.0463, NSP Loss: 0.8474
Epoch 21, Loss: 3.1932, MLM Loss: 2.7228, NSP Loss: 0.4704
Epoch 21, Loss: 3.3917, MLM Loss: 3.0130, NSP Loss: 0.3787
Epoch 21, Loss: 4.2733, MLM Loss: 3.4975, NSP Loss: 0.7757
Epoch 21, Loss: 5.6041, MLM Loss: 4.6297, NSP Loss: 0.9744
Epoch 21, Loss: 3.4752, MLM Loss: 2.6099, NSP Loss: 0.8653
Epoch 21, Loss: 4.5612, MLM Loss: 4.0785, NSP Loss: 0.4827
Epoch 21, Loss: 3.4133, MLM Loss: 2.9456, NSP Loss: 0.4677
Epoch 21, Loss: 5.1129, MLM Loss: 4.0712, NSP Loss: 1.0417
Epoch 21, Loss: 6.0051, MLM Loss: 4.8035, NSP Loss: 1.2016
Epoch 21, Loss: 5.9495, MLM Loss: 4.6072, NSP Loss: 1.3423
Epoch 21, Loss: 4.4042, MLM Loss: 3.6990, NSP Loss: 0.7052
Epoch 31, Loss: 3.6042, MLM Loss: 3.4161, NSP Loss: 0.1881
Epoch 31, Loss: 2.5215, MLM Loss: 2.3122, NSP Loss: 0.2093
Epoch 31, Loss: 4.5753, MLM Loss: 4.3179, NSP Loss: 0.2574
Epoch 31, Loss: 4.6918, MLM Loss: 3.1713, NSP Loss: 1.5205
Epoch 31, Loss: 2.0616, MLM Loss: 1.8776, NSP Loss: 0.1840
Epoch 31, Loss: 2.3950, MLM Loss: 2.1993, NSP Loss: 0.1957
Epoch 31, Loss: 4.2276, MLM Loss: 3.9424, NSP Loss: 0.2853
Epoch 31, Loss: 3.5588, MLM Loss: 3.2606, NSP Loss: 0.2982
Epoch 31, Loss: 6.9618, MLM Loss: 5.7388, NSP Loss: 1.2230
Epoch 31, Loss: 4.7320, MLM Loss: 4.5760, NSP Loss: 0.1560
Epoch 31, Loss: 3.0029, MLM Loss: 2.6581, NSP Loss: 0.3448
Epoch 31, Loss: 6.6682, MLM Loss: 4.6929, NSP Loss: 1.9753
Epoch 31, Loss: 3.7580, MLM Loss: 3.3620, NSP Loss: 0.3960
Epoch 31, Loss: 2.7315, MLM Loss: 2.2884, NSP Loss: 0.4431
Epoch 41, Loss: 6.1012, MLM Loss: 5.0341, NSP Loss: 1.0671
Epoch 41, Loss: 3.8014, MLM Loss: 3.6545, NSP Loss: 0.1469
Epoch 41, Loss: 3.7403, MLM Loss: 3.6762, NSP Loss: 0.0642
Epoch 41, Loss: 3.5076, MLM Loss: 3.4038, NSP Loss: 0.1038
Epoch 41, Loss: 5.5352, MLM Loss: 3.7886, NSP Loss: 1.7466
Epoch 41, Loss: 5.0807, MLM Loss: 5.0402, NSP Loss: 0.0404
Epoch 41, Loss: 5.6927, MLM Loss: 3.7312, NSP Loss: 1.9615
Epoch 41, Loss: 4.0136, MLM Loss: 1.5729, NSP Loss: 2.4407
Epoch 41, Loss: 2.3974, MLM Loss: 2.1449, NSP Loss: 0.2525
Epoch 41, Loss: 5.1592, MLM Loss: 3.4658, NSP Loss: 1.6935
Epoch 41, Loss: 4.4649, MLM Loss: 3.0514, NSP Loss: 1.4135
Epoch 41, Loss: 5.0140, MLM Loss: 3.6168, NSP Loss: 1.3972
Epoch 41, Loss: 2.4383, MLM Loss: 2.2843, NSP Loss: 0.1541
Epoch 41, Loss: 2.5329, MLM Loss: 1.9331, NSP Loss: 0.5998
Epoch 51, Loss: 7.0774, MLM Loss: 6.8978, NSP Loss: 0.1795
Epoch 51, Loss: 1.5395, MLM Loss: 1.2050, NSP Loss: 0.3345
Epoch 51, Loss: 4.9306, MLM Loss: 4.3464, NSP Loss: 0.5842
Epoch 51, Loss: 1.8825, MLM Loss: 0.9295, NSP Loss: 0.9529
Epoch 51, Loss: 3.8173, MLM Loss: 2.4550, NSP Loss: 1.3623
Epoch 51, Loss: 1.1970, MLM Loss: 0.9103, NSP Loss: 0.2868
Epoch 51, Loss: 4.7876, MLM Loss: 3.6723, NSP Loss: 1.1152
Epoch 51, Loss: 1.0099, MLM Loss: 0.6039, NSP Loss: 0.4060
Epoch 51, Loss: 1.8669, MLM Loss: 1.6577, NSP Loss: 0.2092
Epoch 51, Loss: 4.6444, MLM Loss: 4.4716, NSP Loss: 0.1729
Epoch 51, Loss: 1.6767, MLM Loss: 0.6129, NSP Loss: 1.0638
Epoch 51, Loss: 1.6350, MLM Loss: 0.8077, NSP Loss: 0.8274
Epoch 51, Loss: 1.6817, MLM Loss: 1.5437, NSP Loss: 0.1381
Epoch 51, Loss: 3.0002, MLM Loss: 2.0053, NSP Loss: 0.9949
Epoch 61, Loss: 5.4908, MLM Loss: 5.3767, NSP Loss: 0.1141
Epoch 61, Loss: 1.3842, MLM Loss: 0.7242, NSP Loss: 0.6600
Epoch 61, Loss: 5.1134, MLM Loss: 4.1937, NSP Loss: 0.9197
Epoch 61, Loss: 2.5025, MLM Loss: 1.6073, NSP Loss: 0.8952
Epoch 61, Loss: 3.1676, MLM Loss: 2.7547, NSP Loss: 0.4129
Epoch 61, Loss: 2.6773, MLM Loss: 2.3893, NSP Loss: 0.2880
Epoch 61, Loss: 2.2430, MLM Loss: 2.2131, NSP Loss: 0.0299
Epoch 61, Loss: 5.2498, MLM Loss: 4.3278, NSP Loss: 0.9220
Epoch 61, Loss: 2.6416, MLM Loss: 1.7775, NSP Loss: 0.8642
Epoch 61, Loss: 1.1320, MLM Loss: 1.0376, NSP Loss: 0.0944
Epoch 61, Loss: 4.2662, MLM Loss: 2.0571, NSP Loss: 2.2091
Epoch 61, Loss: 3.1929, MLM Loss: 3.1136, NSP Loss: 0.0794
Epoch 61, Loss: 4.0406, MLM Loss: 3.6410, NSP Loss: 0.3996
Epoch 61, Loss: 2.8592, MLM Loss: 2.1883, NSP Loss: 0.6709
Epoch 71, Loss: 3.1688, MLM Loss: 2.9859, NSP Loss: 0.1829
Epoch 71, Loss: 0.4633, MLM Loss: 0.4044, NSP Loss: 0.0589
Epoch 71, Loss: 0.8635, MLM Loss: 0.5831, NSP Loss: 0.2804
Epoch 71, Loss: 1.8514, MLM Loss: 1.1219, NSP Loss: 0.7296
Epoch 71, Loss: 1.5918, MLM Loss: 0.6435, NSP Loss: 0.9484
Epoch 71, Loss: 1.9709, MLM Loss: 0.7322, NSP Loss: 1.2386
Epoch 71, Loss: 6.7886, MLM Loss: 6.2602, NSP Loss: 0.5284
Epoch 71, Loss: 0.4016, MLM Loss: 0.3175, NSP Loss: 0.0840
Epoch 71, Loss: 0.9462, MLM Loss: 0.7725, NSP Loss: 0.1737
Epoch 71, Loss: 1.4485, MLM Loss: 1.2611, NSP Loss: 0.1873
Epoch 71, Loss: 2.2684, MLM Loss: 1.9173, NSP Loss: 0.3511
Epoch 71, Loss: 2.2497, MLM Loss: 0.4204, NSP Loss: 1.8293
Epoch 71, Loss: 0.9488, MLM Loss: 0.7675, NSP Loss: 0.1813
Epoch 71, Loss: 2.1322, MLM Loss: 1.8394, NSP Loss: 0.2928
Epoch 81, Loss: 1.3120, MLM Loss: 0.8094, NSP Loss: 0.5026
Epoch 81, Loss: 2.2443, MLM Loss: 2.0998, NSP Loss: 0.1445
Epoch 81, Loss: 2.1743, MLM Loss: 2.0854, NSP Loss: 0.0889
Epoch 81, Loss: 1.1150, MLM Loss: 0.6782, NSP Loss: 0.4369
Epoch 81, Loss: 6.5734, MLM Loss: 3.8965, NSP Loss: 2.6770
Epoch 81, Loss: 1.1535, MLM Loss: 0.8985, NSP Loss: 0.2550
Epoch 81, Loss: 2.9452, MLM Loss: 2.3414, NSP Loss: 0.6038
Epoch 81, Loss: 2.1704, MLM Loss: 0.4086, NSP Loss: 1.7618
Epoch 81, Loss: 1.2846, MLM Loss: 1.2175, NSP Loss: 0.0672
Epoch 81, Loss: 1.5489, MLM Loss: 1.2531, NSP Loss: 0.2958
Epoch 81, Loss: 2.1183, MLM Loss: 0.7121, NSP Loss: 1.4063
Epoch 81, Loss: 5.0029, MLM Loss: 3.7294, NSP Loss: 1.2735
Epoch 81, Loss: 1.3007, MLM Loss: 1.1846, NSP Loss: 0.1161
Epoch 81, Loss: 3.5184, MLM Loss: 3.2389, NSP Loss: 0.2795
Epoch 91, Loss: 1.5264, MLM Loss: 0.9395, NSP Loss: 0.5869
Epoch 91, Loss: 1.5216, MLM Loss: 0.3422, NSP Loss: 1.1794
Epoch 91, Loss: 2.7438, MLM Loss: 2.4550, NSP Loss: 0.2888
Epoch 91, Loss: 3.2027, MLM Loss: 3.1638, NSP Loss: 0.0389
Epoch 91, Loss: 0.3648, MLM Loss: 0.1236, NSP Loss: 0.2412
Epoch 91, Loss: 1.3834, MLM Loss: 0.2171, NSP Loss: 1.1662
Epoch 91, Loss: 3.0155, MLM Loss: 2.0327, NSP Loss: 0.9828
Epoch 91, Loss: 3.0302, MLM Loss: 2.8876, NSP Loss: 0.1426
Epoch 91, Loss: 2.4716, MLM Loss: 2.1234, NSP Loss: 0.3482
Epoch 91, Loss: 0.9511, MLM Loss: 0.5078, NSP Loss: 0.4433
Epoch 91, Loss: 0.9835, MLM Loss: 0.6809, NSP Loss: 0.3027
Epoch 91, Loss: 2.4609, MLM Loss: 1.9457, NSP Loss: 0.5152
Epoch 91, Loss: 2.1554, MLM Loss: 1.8323, NSP Loss: 0.3231
Epoch 91, Loss: 0.5904, MLM Loss: 0.4430, NSP Loss: 0.1474
Epoch 101, Loss: 3.2188, MLM Loss: 2.6186, NSP Loss: 0.6002
Epoch 101, Loss: 0.6612, MLM Loss: 0.3022, NSP Loss: 0.3590
Epoch 101, Loss: 0.9162, MLM Loss: 0.6775, NSP Loss: 0.2387
Epoch 101, Loss: 0.9508, MLM Loss: 0.3166, NSP Loss: 0.6343
Epoch 101, Loss: 0.5168, MLM Loss: 0.4841, NSP Loss: 0.0327
Epoch 101, Loss: 3.0575, MLM Loss: 3.0242, NSP Loss: 0.0333
Epoch 101, Loss: 1.4720, MLM Loss: 0.5248, NSP Loss: 0.9472
Epoch 101, Loss: 2.4701, MLM Loss: 2.1204, NSP Loss: 0.3498
Epoch 101, Loss: 1.8573, MLM Loss: 1.3200, NSP Loss: 0.5373
Epoch 101, Loss: 1.1186, MLM Loss: 1.0841, NSP Loss: 0.0345
Epoch 101, Loss: 0.9086, MLM Loss: 0.8532, NSP Loss: 0.0554
Epoch 101, Loss: 1.1112, MLM Loss: 0.3313, NSP Loss: 0.7799
Epoch 101, Loss: 5.0888, MLM Loss: 5.0285, NSP Loss: 0.0603
Epoch 101, Loss: 1.1937, MLM Loss: 0.2702, NSP Loss: 0.9235
Epoch 111, Loss: 0.4361, MLM Loss: 0.3562, NSP Loss: 0.0800
Epoch 111, Loss: 0.1946, MLM Loss: 0.1219, NSP Loss: 0.0727
Epoch 111, Loss: 1.2209, MLM Loss: 1.0829, NSP Loss: 0.1380
Epoch 111, Loss: 0.4247, MLM Loss: 0.3745, NSP Loss: 0.0502
Epoch 111, Loss: 0.3759, MLM Loss: 0.3220, NSP Loss: 0.0539
Epoch 111, Loss: 0.2395, MLM Loss: 0.1852, NSP Loss: 0.0543
Epoch 111, Loss: 0.2928, MLM Loss: 0.2633, NSP Loss: 0.0296
Epoch 111, Loss: 1.6823, MLM Loss: 0.1041, NSP Loss: 1.5782
Epoch 111, Loss: 3.3693, MLM Loss: 3.3152, NSP Loss: 0.0541
Epoch 111, Loss: 0.4876, MLM Loss: 0.3233, NSP Loss: 0.1643
Epoch 111, Loss: 0.3873, MLM Loss: 0.1142, NSP Loss: 0.2731
Epoch 111, Loss: 3.5379, MLM Loss: 0.1763, NSP Loss: 3.3616
Epoch 111, Loss: 1.1858, MLM Loss: 0.6898, NSP Loss: 0.4960
Epoch 111, Loss: 0.7442, MLM Loss: 0.1193, NSP Loss: 0.6249
Epoch 121, Loss: 2.0093, MLM Loss: 1.5263, NSP Loss: 0.4829
Epoch 121, Loss: 2.8261, MLM Loss: 2.5207, NSP Loss: 0.3053
Epoch 121, Loss: 1.3235, MLM Loss: 0.5268, NSP Loss: 0.7967
Epoch 121, Loss: 0.3365, MLM Loss: 0.2481, NSP Loss: 0.0884
Epoch 121, Loss: 0.1353, MLM Loss: 0.0634, NSP Loss: 0.0719
Epoch 121, Loss: 1.5244, MLM Loss: 1.1320, NSP Loss: 0.3924
Epoch 121, Loss: 0.9679, MLM Loss: 0.8419, NSP Loss: 0.1261
Epoch 121, Loss: 0.1805, MLM Loss: 0.1108, NSP Loss: 0.0697
Epoch 121, Loss: 0.3634, MLM Loss: 0.0519, NSP Loss: 0.3115
Epoch 121, Loss: 0.9833, MLM Loss: 0.8443, NSP Loss: 0.1390
Epoch 121, Loss: 4.0243, MLM Loss: 3.2574, NSP Loss: 0.7669
Epoch 121, Loss: 1.0404, MLM Loss: 0.8746, NSP Loss: 0.1658
Epoch 121, Loss: 0.5466, MLM Loss: 0.2331, NSP Loss: 0.3135
Epoch 121, Loss: 0.3630, MLM Loss: 0.2762, NSP Loss: 0.0868
Epoch 131, Loss: 0.1499, MLM Loss: 0.1200, NSP Loss: 0.0299
Epoch 131, Loss: 2.2956, MLM Loss: 1.9386, NSP Loss: 0.3570
Epoch 131, Loss: 1.0993, MLM Loss: 0.4645, NSP Loss: 0.6348
Epoch 131, Loss: 3.1251, MLM Loss: 1.0872, NSP Loss: 2.0378
Epoch 131, Loss: 0.9692, MLM Loss: 0.4553, NSP Loss: 0.5139
Epoch 131, Loss: 0.2943, MLM Loss: 0.0593, NSP Loss: 0.2351
Epoch 131, Loss: 3.5025, MLM Loss: 3.4387, NSP Loss: 0.0637
Epoch 131, Loss: 0.3678, MLM Loss: 0.1229, NSP Loss: 0.2449
Epoch 131, Loss: 0.3567, MLM Loss: 0.1309, NSP Loss: 0.2258
Epoch 131, Loss: 2.0889, MLM Loss: 2.0573, NSP Loss: 0.0317
Epoch 131, Loss: 0.0838, MLM Loss: 0.0684, NSP Loss: 0.0153
Epoch 131, Loss: 2.7218, MLM Loss: 2.6849, NSP Loss: 0.0369
Epoch 131, Loss: 0.2239, MLM Loss: 0.0619, NSP Loss: 0.1620
Epoch 131, Loss: 1.6436, MLM Loss: 0.1584, NSP Loss: 1.4852
Epoch 141, Loss: 0.2160, MLM Loss: 0.1309, NSP Loss: 0.0851
Epoch 141, Loss: 0.1957, MLM Loss: 0.0592, NSP Loss: 0.1365
Epoch 141, Loss: 0.5331, MLM Loss: 0.2358, NSP Loss: 0.2973
Epoch 141, Loss: 4.5491, MLM Loss: 4.0179, NSP Loss: 0.5313
Epoch 141, Loss: 0.1072, MLM Loss: 0.0730, NSP Loss: 0.0342
Epoch 141, Loss: 1.2304, MLM Loss: 1.1167, NSP Loss: 0.1137
Epoch 141, Loss: 0.2579, MLM Loss: 0.0404, NSP Loss: 0.2175
Epoch 141, Loss: 0.1679, MLM Loss: 0.1019, NSP Loss: 0.0660
Epoch 141, Loss: 4.0512, MLM Loss: 3.4846, NSP Loss: 0.5666
Epoch 141, Loss: 2.0492, MLM Loss: 2.0071, NSP Loss: 0.0421
Epoch 141, Loss: 2.2333, MLM Loss: 0.3002, NSP Loss: 1.9331
Epoch 141, Loss: 0.4400, MLM Loss: 0.2415, NSP Loss: 0.1984
Epoch 141, Loss: 0.1007, MLM Loss: 0.0367, NSP Loss: 0.0640
Epoch 141, Loss: 1.3038, MLM Loss: 0.4974, NSP Loss: 0.8063
Epoch 151, Loss: 0.7107, MLM Loss: 0.1176, NSP Loss: 0.5931
Epoch 151, Loss: 0.0745, MLM Loss: 0.0576, NSP Loss: 0.0169
Epoch 151, Loss: 0.0661, MLM Loss: 0.0199, NSP Loss: 0.0462
Epoch 151, Loss: 0.4258, MLM Loss: 0.3911, NSP Loss: 0.0346
Epoch 151, Loss: 0.8369, MLM Loss: 0.0712, NSP Loss: 0.7657
Epoch 151, Loss: 1.5684, MLM Loss: 0.8686, NSP Loss: 0.6998
Epoch 151, Loss: 1.2540, MLM Loss: 1.1970, NSP Loss: 0.0570
Epoch 151, Loss: 1.7350, MLM Loss: 0.4622, NSP Loss: 1.2728
Epoch 151, Loss: 0.1029, MLM Loss: 0.0608, NSP Loss: 0.0421
Epoch 151, Loss: 0.9117, MLM Loss: 0.8010, NSP Loss: 0.1107
Epoch 151, Loss: 1.1122, MLM Loss: 1.0766, NSP Loss: 0.0356
Epoch 151, Loss: 0.4695, MLM Loss: 0.1803, NSP Loss: 0.2891
Epoch 151, Loss: 0.7112, MLM Loss: 0.2545, NSP Loss: 0.4566
Epoch 151, Loss: 0.1779, MLM Loss: 0.0716, NSP Loss: 0.1064
Epoch 161, Loss: 0.1942, MLM Loss: 0.0344, NSP Loss: 0.1598
Epoch 161, Loss: 0.0886, MLM Loss: 0.0762, NSP Loss: 0.0124
Epoch 161, Loss: 1.0864, MLM Loss: 0.0782, NSP Loss: 1.0082
Epoch 161, Loss: 0.1117, MLM Loss: 0.0726, NSP Loss: 0.0392
Epoch 161, Loss: 1.7302, MLM Loss: 0.0630, NSP Loss: 1.6672
Epoch 161, Loss: 0.5598, MLM Loss: 0.0294, NSP Loss: 0.5304
Epoch 161, Loss: 2.1245, MLM Loss: 0.1906, NSP Loss: 1.9338
Epoch 161, Loss: 1.1026, MLM Loss: 0.0560, NSP Loss: 1.0466
Epoch 161, Loss: 0.8250, MLM Loss: 0.6550, NSP Loss: 0.1699
Epoch 161, Loss: 0.3814, MLM Loss: 0.1002, NSP Loss: 0.2813
Epoch 161, Loss: 1.1951, MLM Loss: 0.0730, NSP Loss: 1.1220
Epoch 161, Loss: 1.7719, MLM Loss: 0.0355, NSP Loss: 1.7364
Epoch 161, Loss: 0.1371, MLM Loss: 0.0875, NSP Loss: 0.0496
Epoch 161, Loss: 0.2379, MLM Loss: 0.0857, NSP Loss: 0.1521
Epoch 171, Loss: 0.1023, MLM Loss: 0.0333, NSP Loss: 0.0691
Epoch 171, Loss: 0.3404, MLM Loss: 0.0951, NSP Loss: 0.2453
Epoch 171, Loss: 0.0949, MLM Loss: 0.0549, NSP Loss: 0.0400
Epoch 171, Loss: 0.3060, MLM Loss: 0.2661, NSP Loss: 0.0399
Epoch 171, Loss: 0.2058, MLM Loss: 0.1363, NSP Loss: 0.0694
Epoch 171, Loss: 4.1955, MLM Loss: 1.6947, NSP Loss: 2.5008
Epoch 171, Loss: 0.1784, MLM Loss: 0.1172, NSP Loss: 0.0612
Epoch 171, Loss: 0.2492, MLM Loss: 0.0836, NSP Loss: 0.1656
Epoch 171, Loss: 0.0505, MLM Loss: 0.0083, NSP Loss: 0.0422
Epoch 171, Loss: 0.3710, MLM Loss: 0.2911, NSP Loss: 0.0799
Epoch 171, Loss: 2.4526, MLM Loss: 0.7898, NSP Loss: 1.6629
Epoch 171, Loss: 0.3756, MLM Loss: 0.0985, NSP Loss: 0.2772
Epoch 171, Loss: 1.4196, MLM Loss: 0.9281, NSP Loss: 0.4915
Epoch 171, Loss: 2.4393, MLM Loss: 2.0704, NSP Loss: 0.3689
Epoch 181, Loss: 0.0682, MLM Loss: 0.0439, NSP Loss: 0.0243
Epoch 181, Loss: 0.2875, MLM Loss: 0.0146, NSP Loss: 0.2730
Epoch 181, Loss: 1.0931, MLM Loss: 1.0330, NSP Loss: 0.0601
Epoch 181, Loss: 0.3933, MLM Loss: 0.0556, NSP Loss: 0.3378
Epoch 181, Loss: 1.4141, MLM Loss: 0.0528, NSP Loss: 1.3613
Epoch 181, Loss: 1.2546, MLM Loss: 0.1035, NSP Loss: 1.1511
Epoch 181, Loss: 0.3970, MLM Loss: 0.1736, NSP Loss: 0.2235
Epoch 181, Loss: 0.7620, MLM Loss: 0.0682, NSP Loss: 0.6939
Epoch 181, Loss: 0.2274, MLM Loss: 0.1409, NSP Loss: 0.0865
Epoch 181, Loss: 0.2378, MLM Loss: 0.0481, NSP Loss: 0.1897
Epoch 181, Loss: 0.0494, MLM Loss: 0.0416, NSP Loss: 0.0079
Epoch 181, Loss: 0.7730, MLM Loss: 0.7486, NSP Loss: 0.0244
Epoch 181, Loss: 0.0966, MLM Loss: 0.0690, NSP Loss: 0.0276
Epoch 181, Loss: 0.3287, MLM Loss: 0.3184, NSP Loss: 0.0103
Epoch 191, Loss: 2.3749, MLM Loss: 0.3264, NSP Loss: 2.0484
Epoch 191, Loss: 0.9585, MLM Loss: 0.7576, NSP Loss: 0.2009
Epoch 191, Loss: 1.4334, MLM Loss: 0.2052, NSP Loss: 1.2282
Epoch 191, Loss: 0.2663, MLM Loss: 0.0576, NSP Loss: 0.2087
Epoch 191, Loss: 0.0905, MLM Loss: 0.0706, NSP Loss: 0.0199
Epoch 191, Loss: 0.1584, MLM Loss: 0.0450, NSP Loss: 0.1133
Epoch 191, Loss: 1.3412, MLM Loss: 0.0737, NSP Loss: 1.2674
Epoch 191, Loss: 0.0662, MLM Loss: 0.0472, NSP Loss: 0.0189
Epoch 191, Loss: 0.1710, MLM Loss: 0.0376, NSP Loss: 0.1334
Epoch 191, Loss: 0.2292, MLM Loss: 0.0244, NSP Loss: 0.2048
Epoch 191, Loss: 0.3443, MLM Loss: 0.3266, NSP Loss: 0.0177
Epoch 191, Loss: 0.1790, MLM Loss: 0.1368, NSP Loss: 0.0422
Epoch 191, Loss: 0.1733, MLM Loss: 0.1414, NSP Loss: 0.0319
Epoch 191, Loss: 0.0349, MLM Loss: 0.0163, NSP Loss: 0.0186
```

```python
# 推理函数
model.eval()


def generate(tokens):
    input_ids = [word2idx[token] for token in tokens]
    input_ids += [word2idx['[PAD]']] * (MAX_SEQ_LENGTH - len(tokens))
    segment_ids = [0] * 6 + [1] * 5 + [0] * (MAX_SEQ_LENGTH - 11)
    attention_mask = [1] * 6 + [1] * 5 + [0] * (MAX_SEQ_LENGTH - 11)

    input_tensor = torch.LongTensor([input_ids])
    segment_tensor = torch.LongTensor([segment_ids])
    mask_tensor = torch.LongTensor([attention_mask])

    mlm_output, nsp_output = model(input_tensor, segment_tensor, mask_tensor)

    print(f"输入序列: {tokens}")

    # MLM预测
    print("MLM预测:")
    for i, token in enumerate(tokens):
        if token == '[MASK]':
            predicted_id = mlm_output[0][i].argmax().item()
            predicted_word = id2word.get(predicted_id, '[UNK]')
            print(f"位置 {i}: {predicted_word}")

    # NSP预测
    nsp_probs = torch.softmax(nsp_output[0], dim=0)
    nsp_prediction = nsp_output[0].argmax().item()
    result = "是下一句" if nsp_prediction == 1 else "不是下一句"
    confidence = nsp_probs[nsp_prediction].item()

    print(f"NSP预测: {result} (置信度: {confidence:.3f})")


tokens = ['[CLS]', '独', '[MASK]', '寒', '秋', '[SEP]', '湘', '江', '[MASK]', '去', '[SEP]']
generate(tokens)
```

```plaintext
输入序列: ['[CLS]', '独', '[MASK]', '寒', '秋', '[SEP]', '湘', '江', '[MASK]', '去', '[SEP]']
MLM预测:
位置 2: 立
位置 8: 北
NSP预测: 是下一句 (置信度: 0.979)
```

```python
from modelscope import AutoModel

bert_model = AutoModel.from_pretrained("google-bert/bert-base-uncased")

print(bert_model)
```

```plaintext
Downloading Model from https://www.modelscope.cn to directory: /Users/dadudu/.cache/modelscope/hub/models/google-bert/bert-base-uncased
BertModel(
  (embeddings): BertEmbeddings(
    (word_embeddings): Embedding(30522, 768, padding_idx=0)
    (position_embeddings): Embedding(512, 768)
    (token_type_embeddings): Embedding(2, 768)
    (LayerNorm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
    (dropout): Dropout(p=0.1, inplace=False)
  )
  (encoder): BertEncoder(
    (layer): ModuleList(
      (0-11): 12 x BertLayer(
        (attention): BertAttention(
          (self): BertSdpaSelfAttention(
            (query): Linear(in_features=768, out_features=768, bias=True)
            (key): Linear(in_features=768, out_features=768, bias=True)
            (value): Linear(in_features=768, out_features=768, bias=True)
            (dropout): Dropout(p=0.1, inplace=False)
          )
          (output): BertSelfOutput(
            (dense): Linear(in_features=768, out_features=768, bias=True)
            (LayerNorm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
            (dropout): Dropout(p=0.1, inplace=False)
          )
        )
        (intermediate): BertIntermediate(
          (dense): Linear(in_features=768, out_features=3072, bias=True)
          (intermediate_act_fn): GELUActivation()
        )
        (output): BertOutput(
          (dense): Linear(in_features=3072, out_features=768, bias=True)
          (LayerNorm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
          (dropout): Dropout(p=0.1, inplace=False)
        )
      )
    )
  )
  (pooler): BertPooler(
    (dense): Linear(in_features=768, out_features=768, bias=True)
    (activation): Tanh()
  )
)
```

```python
# 模拟一下前向传播
input_ids = torch.tensor([[101, 2000, 2001, 2002, 102]])
output = bert_model(input_ids)
print(output)
```

```plaintext
BaseModelOutputWithPoolingAndCrossAttentions(last_hidden_state=tensor([[[-0.1281,  0.0838, -0.0971,  ..., -0.1780,  0.2228,  0.1767],
         [-0.0450, -0.1157,  0.0632,  ..., -0.1008,  0.3414,  0.0258],
         [-0.5051, -0.2228, -0.4401,  ..., -0.0853,  0.1235,  0.0453],
         [-0.0954, -0.2971, -0.1683,  ..., -0.1606,  0.4915, -0.0244],
         [ 0.5949,  0.1752, -0.2684,  ...,  0.1255, -0.7818, -0.3832]]],
       grad_fn=<NativeLayerNormBackward0>), pooler_output=tensor([[-7.7866e-01, -9.6673e-02,  6.1602e-01,  6.1991e-01, -5.2838e-01,
         -5.2755e-02,  8.7809e-01,  2.2782e-01,  3.9066e-01, -9.9922e-01,
          2.4110e-01, -9.0804e-02,  9.5849e-01, -3.1271e-01,  8.7413e-01,
         -4.6824e-01, -1.7867e-01, -4.3782e-01,  2.6917e-01, -7.9387e-01,
          5.2225e-01,  5.7683e-01,  6.0155e-01,  1.7334e-01,  1.9879e-01,
         -2.1064e-01, -4.9724e-01,  8.7504e-01,  9.2471e-01,  5.8795e-01,
         -6.0665e-01,  2.8890e-02, -9.5917e-01, -1.0064e-01,  4.8571e-01,
         -9.5719e-01,  2.8400e-03, -5.9998e-01,  4.6330e-02,  9.3878e-02,
         -7.5704e-01,  3.4776e-02,  9.8407e-01, -4.2260e-01, -1.1437e-01,
         -3.0513e-01, -9.9709e-01,  1.3263e-01, -7.7565e-01, -5.7222e-01,
         -3.7024e-01, -6.6764e-01,  3.9487e-02,  2.5560e-01,  2.8312e-01,
          5.1256e-01, -2.0879e-01,  9.6594e-02,  1.7961e-02, -3.8508e-01,
         -4.6578e-01,  1.5848e-01,  3.6269e-01, -8.3004e-01, -4.2721e-01,
         -6.1985e-01, -2.0700e-02, -1.1455e-01,  6.5942e-02, -8.8949e-02,
          7.6604e-01,  6.8939e-02,  4.2837e-01, -7.0934e-01, -5.6274e-01,
          8.4588e-02, -4.2800e-01,  9.9981e-01, -3.5772e-01, -9.3997e-01,
         -5.3635e-01, -3.1606e-01,  3.4677e-01,  6.5122e-01, -5.1726e-01,
         -9.9925e-01,  1.2396e-01, -5.1711e-02, -9.7207e-01,  1.1132e-01,
          1.4265e-01, -3.3971e-02, -4.8118e-01,  3.4374e-01, -2.9450e-01,
         -5.5926e-02, -8.7391e-02,  4.7654e-01, -6.6568e-02,  1.0182e-01,
         -7.1573e-02, -1.1578e-01,  1.1627e-01, -2.2560e-01,  1.2111e-03,
         -2.2144e-01, -4.2738e-01,  1.0090e-01, -2.9164e-01,  4.3841e-01,
          2.5211e-01, -1.3522e-01,  1.7720e-01, -8.9523e-01,  4.6953e-01,
         -8.6282e-02, -9.5629e-01, -3.5912e-01, -9.6323e-01,  5.1518e-01,
          1.0010e-01, -2.3391e-02,  9.1019e-01,  5.7585e-01,  1.8540e-01,
          3.4549e-02,  5.9073e-01, -9.9992e-01, -1.7408e-01, -1.1912e-01,
          2.8831e-01, -3.9999e-02, -9.3171e-01, -8.9677e-01,  3.9708e-01,
          8.9621e-01,  6.0274e-02,  9.7292e-01, -1.2731e-01,  8.6653e-01,
          2.3733e-01, -5.0983e-02, -4.3204e-01, -3.6070e-01,  2.5261e-01,
          4.0758e-01, -4.5477e-01,  1.7861e-01,  2.0306e-01, -3.1011e-01,
          1.1922e-01, -1.5754e-01,  3.2886e-01, -8.5997e-01, -2.9335e-01,
          9.0014e-01,  3.6367e-01,  5.0835e-01,  6.1515e-01, -1.7130e-01,
         -2.6644e-01,  7.0946e-01,  2.0513e-01,  2.0883e-01,  5.2318e-02,
          2.8068e-01, -2.3088e-01,  2.2330e-01, -7.2000e-01,  3.9976e-01,
          2.5764e-01, -6.9546e-02,  4.5106e-01, -9.2816e-01, -1.2908e-01,
          2.6470e-01,  9.7088e-01,  6.6655e-01,  8.7772e-02, -2.8896e-01,
         -1.5879e-01, -4.2645e-02, -8.7256e-01,  9.3801e-01, -4.5867e-02,
          1.4562e-01,  6.9260e-01, -3.2147e-01, -7.7608e-01, -4.2071e-01,
          7.4827e-01,  2.8402e-01, -7.3349e-01,  1.0784e-01, -3.8339e-01,
         -2.5954e-01,  3.5751e-01,  3.6364e-01, -1.7642e-01, -3.0899e-01,
          6.8049e-02,  8.3702e-01,  9.4424e-01,  6.7916e-01, -5.9726e-01,
          4.7670e-01, -8.0644e-01, -3.0988e-01, -1.9440e-02,  1.6423e-01,
          2.2786e-02,  9.7781e-01,  2.5625e-01,  7.7096e-03, -8.6636e-01,
         -9.6017e-01, -1.0493e-02, -8.3269e-01,  1.1680e-01, -4.1758e-01,
          7.0012e-02,  8.2417e-01, -3.3864e-01,  2.5358e-01, -9.6035e-01,
         -7.3913e-01,  2.1553e-01, -1.7967e-01,  2.4684e-01, -9.3825e-02,
         -2.7901e-01, -3.0725e-01, -3.1134e-01,  7.2395e-01,  8.0219e-01,
          5.7752e-01, -5.6330e-01,  8.1760e-01, -1.7123e-01,  7.8284e-01,
         -4.2943e-01,  9.2455e-01, -2.7840e-01,  2.3454e-01, -8.3420e-01,
          3.9047e-01, -8.0997e-01,  2.4875e-01,  2.7483e-02, -6.6150e-01,
         -4.1827e-01,  3.6176e-01,  6.0748e-02,  7.6649e-01, -3.7764e-01,
          9.8581e-01,  3.2328e-01, -8.9645e-01,  6.2373e-01,  7.6959e-02,
         -9.6225e-01, -3.2324e-01,  2.2231e-01, -7.4533e-01, -1.5738e-01,
         -2.9632e-01, -8.8781e-01,  7.8920e-01,  9.6534e-02,  9.7146e-01,
          4.4106e-01, -8.5484e-01, -5.6031e-02, -7.7975e-01, -2.5462e-01,
          2.8989e-02,  6.8624e-01, -2.2008e-01, -9.1993e-01,  3.4641e-01,
          4.0289e-01,  2.4546e-01,  6.8470e-01,  9.8007e-01,  9.7274e-01,
          9.3480e-01,  8.0904e-01,  7.6006e-01, -2.7955e-01,  4.5449e-01,
          9.9957e-01,  7.1130e-04, -9.9784e-01, -9.0553e-01, -3.6525e-01,
          3.3785e-01, -9.9990e-01, -6.0838e-02,  9.7102e-02, -8.3726e-01,
         -4.2872e-01,  9.3719e-01,  9.5882e-01, -9.9961e-01,  7.6088e-01,
          8.7383e-01, -4.5013e-01, -2.5663e-01, -3.7466e-02,  9.3224e-01,
          2.9799e-01,  1.6307e-01, -1.3711e-01,  1.6455e-01,  1.9489e-01,
         -7.4643e-01,  4.0319e-01,  5.0645e-01, -3.0182e-01,  8.6802e-02,
         -6.0982e-01, -8.4795e-01, -3.6792e-01, -3.6632e-02, -3.1456e-01,
         -9.1956e-01,  5.6878e-02, -4.2941e-01,  5.1485e-01,  4.1981e-03,
          1.1682e-01, -6.9495e-01,  4.7406e-02, -6.0509e-01,  2.1057e-01,
          4.8105e-01, -8.4487e-01, -5.9248e-01, -1.1192e-01, -5.4769e-01,
          3.9151e-01, -8.8701e-01,  9.3176e-01, -2.6097e-01, -4.4948e-01,
          9.9969e-01, -4.4808e-01, -7.7033e-01,  2.4743e-01,  4.6868e-02,
          8.0169e-03,  9.9952e-01,  3.0561e-01, -9.3631e-01, -3.6149e-01,
         -5.3447e-02, -1.7728e-01, -1.0991e-01,  9.9097e-01, -5.5198e-02,
          5.0250e-01,  4.9476e-01,  9.2097e-01, -9.6566e-01, -3.5954e-01,
         -8.2746e-01, -9.1728e-01,  9.2045e-01,  8.5849e-01, -1.1219e-01,
         -4.2687e-01,  1.7306e-02,  1.6477e-01,  1.6057e-01, -9.0920e-01,
          5.4957e-01,  3.6105e-01, -8.0672e-02,  8.2733e-01, -8.1622e-01,
         -3.5612e-01,  2.7540e-01,  7.7868e-02,  4.3077e-01, -4.2028e-01,
          3.7010e-01, -1.4282e-01,  2.7161e-02, -1.7258e-01,  4.0384e-01,
         -9.4235e-01, -1.5178e-01,  9.9939e-01,  1.4334e-01, -6.9941e-01,
         -5.6942e-02, -1.1847e-02, -4.3611e-01,  1.3160e-01,  2.3689e-01,
         -2.2373e-01, -6.8968e-01, -3.9084e-01, -8.7683e-01, -9.6226e-01,
          6.5971e-01,  1.2896e-01, -1.5912e-01,  9.8481e-01,  1.8975e-01,
         -1.6855e-02, -3.6467e-01, -3.6964e-01,  3.4179e-02,  4.3758e-01,
         -6.5705e-01,  9.3171e-01, -1.5830e-01,  3.4773e-01,  7.5903e-01,
          4.8638e-01, -1.9564e-01, -4.7777e-01, -1.4214e-01, -8.4334e-01,
          1.1933e-01, -8.9993e-01,  9.1737e-01, -6.5234e-01,  1.3594e-01,
         -4.6837e-03, -1.9657e-01,  9.9955e-01,  4.5773e-01,  4.8221e-01,
         -4.8250e-01,  8.2677e-01, -1.0343e-01, -6.8372e-01, -1.8687e-01,
          9.7954e-02,  5.4608e-01, -4.5051e-02,  1.0774e-01, -9.2793e-01,
         -5.3415e-01, -4.2264e-01, -9.3683e-01, -9.7373e-01,  6.4985e-01,
          7.5766e-01, -1.5643e-02,  3.9277e-01, -4.0846e-01, -4.7790e-01,
         -4.5419e-02, -1.0059e-01, -8.7107e-01,  6.2736e-01, -1.7426e-01,
          2.5138e-01, -1.6836e-01,  3.8703e-01, -5.9445e-01,  7.7968e-01,
          7.3896e-01,  1.9524e-01, -4.9162e-02, -6.9122e-01,  6.7256e-01,
         -7.0607e-01,  4.7364e-01, -8.5782e-02,  9.9985e-01, -3.0814e-01,
         -3.1658e-01,  6.5836e-01,  4.7689e-01,  1.8601e-02,  1.2584e-01,
         -4.2013e-01,  7.9506e-02,  4.4144e-01,  6.4267e-01, -7.7465e-01,
         -1.7053e-01,  4.0024e-01, -6.3954e-01, -3.7914e-01,  6.2228e-01,
         -3.2280e-01, -8.3422e-02,  5.7571e-02,  3.5642e-02,  9.9194e-01,
         -5.6089e-02,  4.5232e-02, -3.0466e-01,  7.9963e-02, -1.4525e-01,
         -4.8915e-01,  9.9768e-01,  2.4149e-01, -3.1113e-01, -9.6960e-01,
          4.4438e-01, -8.3810e-01,  9.1019e-01,  6.5950e-01, -7.3455e-01,
          3.2826e-01,  3.0449e-01, -1.3333e-01,  5.3793e-01, -7.7750e-02,
         -1.6841e-01,  1.2235e-02,  8.1599e-02,  8.9765e-01, -2.5590e-01,
         -9.0323e-01, -4.4431e-01,  1.2655e-01, -8.8965e-01,  3.4829e-01,
         -3.2328e-01, -6.9106e-02, -5.2382e-02,  6.3276e-01,  7.8918e-01,
         -1.3164e-01, -9.4732e-01, -1.3761e-02, -9.0895e-02,  9.1754e-01,
          5.4933e-02, -4.2913e-01, -8.6106e-01, -6.0605e-01, -2.4665e-01,
          5.7654e-01, -8.5516e-01,  9.1571e-01, -9.5638e-01,  1.9570e-01,
          9.9875e-01,  1.4525e-01, -7.3273e-01,  2.0830e-02, -2.8658e-01,
          4.1932e-02,  2.7292e-01,  5.8271e-01, -8.8625e-01, -6.7288e-02,
          7.9535e-02,  1.6544e-01, -6.8728e-02,  3.3702e-01,  5.5424e-01,
          2.7405e-02, -3.4087e-01, -3.4605e-01,  1.4054e-02,  2.6675e-01,
          6.1100e-01, -2.0853e-01, -6.6543e-02,  4.3263e-02, -1.4878e-02,
         -8.4525e-01, -6.2033e-02, -2.9510e-02, -7.0869e-01,  5.2580e-01,
         -9.9980e-01, -5.1790e-01, -5.9656e-01, -1.6047e-01,  7.5491e-01,
         -3.7248e-01, -7.7064e-02, -5.7914e-01,  4.9885e-01,  8.5022e-01,
          6.2704e-01, -3.1629e-02,  2.6361e-01, -6.2252e-01, -9.1453e-03,
          3.4899e-02, -8.3837e-03,  2.9834e-01,  6.4392e-01, -4.5877e-02,
          9.9992e-01, -3.8349e-02, -3.5290e-01, -9.3257e-01,  1.3437e-01,
         -1.3897e-01,  9.7973e-01, -8.2331e-01, -8.6531e-01,  1.1777e-01,
         -2.1437e-01, -7.0864e-01,  6.8108e-02, -8.1472e-03, -3.2792e-01,
          3.2182e-01,  9.1834e-01,  8.5842e-01, -3.5615e-01,  1.5316e-01,
         -2.1138e-01, -2.6605e-01,  2.4465e-02, -6.3432e-01,  9.5946e-01,
         -5.4406e-03,  7.4890e-01,  8.3067e-01,  2.5438e-01,  9.1203e-01,
          5.7083e-02,  6.4306e-01,  4.6942e-02,  9.9841e-01,  1.8413e-01,
         -8.4383e-01,  4.4109e-01, -9.6085e-01, -3.1353e-02, -8.9065e-01,
          1.3427e-01,  2.1224e-02,  7.3413e-01, -7.4305e-02,  9.1128e-01,
          6.9170e-01, -9.9893e-02,  2.4625e-01,  6.4577e-01,  2.4055e-01,
         -8.4375e-01, -9.5587e-01, -9.6176e-01,  4.6447e-02, -3.1159e-01,
          3.8409e-02,  1.3868e-01,  4.0251e-02,  1.2410e-01,  1.7243e-01,
         -9.9719e-01,  8.3925e-01,  2.7634e-01, -4.5846e-01,  8.9313e-01,
          2.6528e-02, -5.9444e-03,  1.5696e-01, -9.6106e-01, -9.0699e-01,
         -1.5568e-01, -1.8821e-01,  6.4485e-01,  4.1350e-01,  7.9011e-01,
          1.6770e-01, -4.4108e-01,  1.1135e-01,  4.2088e-01,  4.4733e-01,
         -9.7429e-01,  3.0186e-01,  4.6379e-01, -8.9535e-01,  8.9919e-01,
         -4.5490e-01, -1.4046e-01,  6.4508e-01,  3.9589e-01,  8.8305e-01,
          5.8715e-01,  3.5091e-01,  7.9424e-02,  3.2719e-01,  7.8549e-01,
          9.0970e-01,  9.7004e-01,  3.6949e-01,  6.9336e-01,  5.1763e-01,
          2.1515e-01,  2.2673e-01, -8.5309e-01, -8.8016e-03, -3.0995e-01,
         -1.1526e-01,  7.3837e-02, -8.8352e-02, -9.0401e-01,  6.0089e-01,
         -8.8071e-02,  2.4857e-01, -2.5871e-01,  1.6967e-01, -2.9333e-01,
         -1.5332e-01, -6.1366e-01, -2.2538e-01,  4.6078e-01,  2.5084e-01,
          8.2423e-01, -2.2106e-01,  6.4997e-02, -3.9216e-01,  5.8304e-03,
          4.2209e-01, -8.3684e-01,  8.0362e-01,  8.9380e-02,  4.2275e-01,
         -4.6015e-01, -1.1285e-01,  3.7771e-01, -4.4537e-01, -2.0926e-01,
         -1.4287e-01, -5.7502e-01,  7.0937e-01,  1.0635e-01, -2.8463e-01,
         -3.2010e-01,  3.6384e-01,  2.1166e-01,  5.9951e-01,  3.5877e-01,
          4.7581e-01,  1.2860e-01, -3.9890e-02,  1.7779e-01, -2.3096e-01,
         -9.9682e-01,  2.5743e-01,  4.6656e-01, -3.0753e-01,  2.7875e-01,
         -4.6807e-01,  2.4296e-01, -9.2775e-01,  1.7689e-05, -5.2461e-01,
         -4.5225e-01, -3.6694e-01, -6.9290e-02,  3.7443e-01,  6.4771e-01,
         -3.3905e-01,  7.7335e-01,  2.4197e-01,  5.9398e-01,  4.5984e-01,
          3.8435e-01, -4.8714e-01,  7.8396e-01]], grad_fn=<TanhBackward0>), hidden_states=None, past_key_values=None, attentions=None, cross_attentions=None)
```

```python

mlm_criterion = nn.CrossEntropyLoss(ignore_index=-100)
mlm_criterion(torch.tensor([[0.1, 0.8, 0.1], [0.1, 0.2, 70]]), torch.tensor([1, -100]))
```

```plaintext
tensor(0.6897)
```