# 11、Word2Vec之SkipGram实战

Word2Vec分两种：

- Continuous Skip-gram (CSG)：跳词模型，给定中心词，预测周围词
- Continuous Bag-of-Words (CBoW)：连续的词袋模型，给定周围词，预测中心词

通过Word2Vec的方式来训练模型，最终既能学到词向量，也能学到词之间的语义关系。

### Skip-gram

```python
# 语料
texts = [
    "I love natural language processing.",
    "I love machine learning.",
    "I love coding in Python and Java.",
    "I love Java.",
    "I don't love Java."
]

sentences = [text.split() for text in texts]
sentences
```

```plaintext
[['I', 'love', 'natural', 'language', 'processing.'],
 ['I', 'love', 'machine', 'learning.'],
 ['I', 'love', 'coding', 'in', 'Python', 'and', 'Java.'],
 ['I', 'love', 'Java.'],
 ['I', "don't", 'love', 'Java.']]
```

Skip-gram要做的是给定中心词，预测周围词，比如窗口大小为2时：

1. 给定"I"，预测"love"和"natural"
2. 给定"love"，预测"I"和"natural"和"language"
3. 给定"natural"，预测"I"、"love"、"language"和"processing"

窗口大小为2，表示中心词左右两边的2个词。

这样就能学到每个词的向量表示和词与词之间的语义关系。

```python
# 词汇表
vocabulary = {}
for sentence in sentences:
    for word in sentence:
        if word not in vocabulary:
            vocabulary[word] = len(vocabulary)

vocab_size = len(vocabulary)  # 词汇表大小
vocabulary
```

```plaintext
{'I': 0,
 'love': 1,
 'natural': 2,
 'language': 3,
 'processing.': 4,
 'machine': 5,
 'learning.': 6,
 'coding': 7,
 'in': 8,
 'Python': 9,
 'and': 10,
 'Java.': 11,
 "don't": 12}
```

## One-hot编码

```python
def one_hot(idx, vocab_size):
    one_hot = torch.zeros(vocab_size)
    one_hot[idx] = 1
    return one_hot

one_hot(vocabulary['learning.'], vocab_size), one_hot(vocabulary['and'], vocab_size)
```

```plaintext
(tensor([0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.]),
 tensor([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.]))
```

```python
import torch

# 生成训练数据
def generate_training_data(sentences, window_size):
    center_words = []
    target_words = []

    for sentence in sentences:
        indices = [vocabulary[word] for word in sentence]
        for center_pos in range(len(indices)):
            # 确定上下文窗口范围
            start = max(0, center_pos - window_size)
            end = min(len(indices), center_pos + window_size + 1)

            # 收集上下文词
            for context_pos in range(start, end):
                if context_pos != center_pos:
                    center_words.append(indices[center_pos])
                    target_words.append(indices[context_pos])

    return torch.LongTensor(center_words), torch.LongTensor(target_words)


WINDOW_SIZE = 2
center_words, target_words = generate_training_data(sentences, WINDOW_SIZE)

center_words, target_words
```

```plaintext
(tensor([ 0,  0,  1,  1,  1,  2,  2,  2,  2,  3,  3,  3,  4,  4,  0,  0,  1,  1,
          1,  5,  5,  5,  6,  6,  0,  0,  1,  1,  1,  7,  7,  7,  7,  8,  8,  8,
          8,  9,  9,  9,  9, 10, 10, 10, 11, 11,  0,  0,  1,  1, 11, 11,  0,  0,
         12, 12, 12,  1,  1,  1, 11, 11]),
 tensor([ 1,  2,  0,  2,  3,  0,  1,  3,  4,  1,  2,  4,  2,  3,  1,  5,  0,  5,
          6,  0,  1,  6,  1,  5,  1,  7,  0,  7,  8,  0,  1,  8,  9,  1,  7,  9,
         10,  7,  8, 10, 11,  8,  9, 11,  9, 10,  1, 11,  0, 11,  0,  1, 12,  1,
          0,  1, 11,  0, 12, 11, 12,  1]))
```

```python
from torch.utils.data import TensorDataset, DataLoader

dataset = TensorDataset(center_words, target_words)
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)
```

## 定义模型

```python
from torch import nn
from torch import optim

class SkipGram(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()

        self.input_embed = nn.Linear(vocab_size, embedding_dim, bias=False)    # y=wx  13*100
        self.output_embed = nn.Linear(embedding_dim, vocab_size, bias=False)   # y=wx  100*13

    def forward(self, center_word):
        center_word_one_hot = one_hot(center_word, vocab_size).view(1, -1)

        hidden = self.input_embed(center_word_one_hot)
        return self.output_embed(hidden)


EMBEDDING_DIM = 10

# 初始化模型、损失函数和优化器
model = SkipGram(vocab_size, EMBEDDING_DIM)
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()


# 开始训练
EPOCHS = 10

for epoch in range(EPOCHS):
    for center_batch, target_batch in dataloader:
        predict = model(center_batch)
        loss = criterion(predict, target_batch)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch + 1}/{EPOCHS}, Loss: {loss:.4f}")
```

```plaintext
Epoch 1/10, Loss: 2.6427
Epoch 1/10, Loss: 2.5813
Epoch 1/10, Loss: 2.5834
Epoch 1/10, Loss: 2.4585
Epoch 1/10, Loss: 2.6689
Epoch 1/10, Loss: 2.4673
Epoch 1/10, Loss: 2.5597
Epoch 1/10, Loss: 2.5322
Epoch 1/10, Loss: 2.6578
Epoch 1/10, Loss: 2.6455
Epoch 1/10, Loss: 2.6362
Epoch 1/10, Loss: 2.5229
Epoch 1/10, Loss: 2.7105
Epoch 1/10, Loss: 2.6132
Epoch 1/10, Loss: 2.6768
Epoch 1/10, Loss: 2.5622
Epoch 1/10, Loss: 2.3861
Epoch 1/10, Loss: 2.5440
Epoch 1/10, Loss: 2.4837
Epoch 1/10, Loss: 2.6077
Epoch 1/10, Loss: 2.5869
Epoch 1/10, Loss: 2.5705
Epoch 1/10, Loss: 2.4208
Epoch 1/10, Loss: 2.6558
Epoch 1/10, Loss: 2.5567
Epoch 1/10, Loss: 2.5931
Epoch 1/10, Loss: 2.7321
Epoch 1/10, Loss: 2.6022
Epoch 1/10, Loss: 2.5126
Epoch 1/10, Loss: 2.5887
Epoch 1/10, Loss: 2.4937
Epoch 1/10, Loss: 2.5391
Epoch 1/10, Loss: 2.5577
Epoch 1/10, Loss: 2.6170
Epoch 1/10, Loss: 2.4745
Epoch 1/10, Loss: 2.5042
Epoch 1/10, Loss: 2.5349
Epoch 1/10, Loss: 2.5637
Epoch 1/10, Loss: 2.6511
Epoch 1/10, Loss: 2.6319
Epoch 1/10, Loss: 2.5602
Epoch 1/10, Loss: 2.6398
Epoch 1/10, Loss: 2.6023
Epoch 1/10, Loss: 2.6931
Epoch 1/10, Loss: 2.5973
Epoch 1/10, Loss: 2.5653
Epoch 1/10, Loss: 2.5250
Epoch 1/10, Loss: 2.4671
Epoch 1/10, Loss: 2.6518
Epoch 1/10, Loss: 2.5574
Epoch 1/10, Loss: 2.6311
Epoch 1/10, Loss: 2.5518
Epoch 1/10, Loss: 2.6076
Epoch 1/10, Loss: 2.4942
Epoch 1/10, Loss: 2.6629
Epoch 1/10, Loss: 2.6276
Epoch 1/10, Loss: 2.4738
Epoch 1/10, Loss: 2.5932
Epoch 1/10, Loss: 2.4954
Epoch 1/10, Loss: 2.5130
Epoch 1/10, Loss: 2.6240
Epoch 1/10, Loss: 2.5888
Epoch 2/10, Loss: 2.6008
Epoch 2/10, Loss: 2.4647
Epoch 2/10, Loss: 2.6195
Epoch 2/10, Loss: 2.5083
Epoch 2/10, Loss: 2.5881
Epoch 2/10, Loss: 2.5505
Epoch 2/10, Loss: 2.5560
Epoch 2/10, Loss: 2.5203
Epoch 2/10, Loss: 2.5823
Epoch 2/10, Loss: 2.4725
Epoch 2/10, Loss: 2.5703
Epoch 2/10, Loss: 2.5575
Epoch 2/10, Loss: 2.6380
Epoch 2/10, Loss: 2.5078
Epoch 2/10, Loss: 2.4865
Epoch 2/10, Loss: 2.6113
Epoch 2/10, Loss: 2.5838
Epoch 2/10, Loss: 2.5544
Epoch 2/10, Loss: 2.6717
Epoch 2/10, Loss: 2.6235
Epoch 2/10, Loss: 2.5828
Epoch 2/10, Loss: 2.5402
Epoch 2/10, Loss: 2.5314
Epoch 2/10, Loss: 2.3811
Epoch 2/10, Loss: 2.5693
Epoch 2/10, Loss: 2.6162
Epoch 2/10, Loss: 2.4911
Epoch 2/10, Loss: 2.7064
Epoch 2/10, Loss: 2.5857
Epoch 2/10, Loss: 2.6108
Epoch 2/10, Loss: 2.4727
Epoch 2/10, Loss: 2.6686
Epoch 2/10, Loss: 2.5434
Epoch 2/10, Loss: 2.6029
Epoch 2/10, Loss: 2.5563
Epoch 2/10, Loss: 2.5565
Epoch 2/10, Loss: 2.4518
Epoch 2/10, Loss: 2.6896
Epoch 2/10, Loss: 2.4907
Epoch 2/10, Loss: 2.4783
Epoch 2/10, Loss: 2.4717
Epoch 2/10, Loss: 2.6541
Epoch 2/10, Loss: 2.7307
Epoch 2/10, Loss: 2.5017
Epoch 2/10, Loss: 2.6444
Epoch 2/10, Loss: 2.5197
Epoch 2/10, Loss: 2.6060
Epoch 2/10, Loss: 2.5728
Epoch 2/10, Loss: 2.6460
Epoch 2/10, Loss: 2.5260
Epoch 2/10, Loss: 2.4124
Epoch 2/10, Loss: 2.5795
Epoch 2/10, Loss: 2.5747
Epoch 2/10, Loss: 2.5818
Epoch 2/10, Loss: 2.6346
Epoch 2/10, Loss: 2.6595
Epoch 2/10, Loss: 2.5585
Epoch 2/10, Loss: 2.6006
Epoch 2/10, Loss: 2.6572
Epoch 2/10, Loss: 2.5685
Epoch 2/10, Loss: 2.5804
Epoch 2/10, Loss: 2.5617
Epoch 3/10, Loss: 2.4970
Epoch 3/10, Loss: 2.6855
Epoch 3/10, Loss: 2.5641
Epoch 3/10, Loss: 2.6643
Epoch 3/10, Loss: 2.5594
Epoch 3/10, Loss: 2.7034
Epoch 3/10, Loss: 2.6423
Epoch 3/10, Loss: 2.6540
Epoch 3/10, Loss: 2.5022
Epoch 3/10, Loss: 2.6532
Epoch 3/10, Loss: 2.5715
Epoch 3/10, Loss: 2.5761
Epoch 3/10, Loss: 2.5750
Epoch 3/10, Loss: 2.6650
Epoch 3/10, Loss: 2.4904
Epoch 3/10, Loss: 2.5505
Epoch 3/10, Loss: 2.5526
Epoch 3/10, Loss: 2.5417
Epoch 3/10, Loss: 2.5467
Epoch 3/10, Loss: 2.5534
Epoch 3/10, Loss: 2.5801
Epoch 3/10, Loss: 2.5508
Epoch 3/10, Loss: 2.6376
Epoch 3/10, Loss: 2.5555
Epoch 3/10, Loss: 2.6055
Epoch 3/10, Loss: 2.6168
Epoch 3/10, Loss: 2.5935
Epoch 3/10, Loss: 2.5159
Epoch 3/10, Loss: 2.5347
Epoch 3/10, Loss: 2.5413
Epoch 3/10, Loss: 2.5705
Epoch 3/10, Loss: 2.4739
Epoch 3/10, Loss: 2.4474
Epoch 3/10, Loss: 2.4807
Epoch 3/10, Loss: 2.5132
Epoch 3/10, Loss: 2.5698
Epoch 3/10, Loss: 2.6359
Epoch 3/10, Loss: 2.3765
Epoch 3/10, Loss: 2.6498
Epoch 3/10, Loss: 2.5911
Epoch 3/10, Loss: 2.6285
Epoch 3/10, Loss: 2.5497
Epoch 3/10, Loss: 2.4891
Epoch 3/10, Loss: 2.7266
Epoch 3/10, Loss: 2.5202
Epoch 3/10, Loss: 2.5698
Epoch 3/10, Loss: 2.5851
Epoch 3/10, Loss: 2.5797
Epoch 3/10, Loss: 2.5502
Epoch 3/10, Loss: 2.4732
Epoch 3/10, Loss: 2.6034
Epoch 3/10, Loss: 2.5449
Epoch 3/10, Loss: 2.5585
Epoch 3/10, Loss: 2.4054
Epoch 3/10, Loss: 2.5132
Epoch 3/10, Loss: 2.5751
Epoch 3/10, Loss: 2.5683
Epoch 3/10, Loss: 2.4643
Epoch 3/10, Loss: 2.4801
Epoch 3/10, Loss: 2.5758
Epoch 3/10, Loss: 2.6068
Epoch 3/10, Loss: 2.4739
Epoch 4/10, Loss: 2.6510
Epoch 4/10, Loss: 2.5514
Epoch 4/10, Loss: 2.5720
Epoch 4/10, Loss: 2.5762
Epoch 4/10, Loss: 2.5150
Epoch 4/10, Loss: 2.3712
Epoch 4/10, Loss: 2.5687
Epoch 4/10, Loss: 2.6236
Epoch 4/10, Loss: 2.6817
Epoch 4/10, Loss: 2.4740
Epoch 4/10, Loss: 2.5079
Epoch 4/10, Loss: 2.4703
Epoch 4/10, Loss: 2.6223
Epoch 4/10, Loss: 2.4863
Epoch 4/10, Loss: 2.5720
Epoch 4/10, Loss: 2.4962
Epoch 4/10, Loss: 2.6401
Epoch 4/10, Loss: 2.4611
Epoch 4/10, Loss: 2.5705
Epoch 4/10, Loss: 2.6471
Epoch 4/10, Loss: 2.5670
Epoch 4/10, Loss: 2.6613
Epoch 4/10, Loss: 2.5402
Epoch 4/10, Loss: 2.5609
Epoch 4/10, Loss: 2.5356
Epoch 4/10, Loss: 2.5419
Epoch 4/10, Loss: 2.5530
Epoch 4/10, Loss: 2.5692
Epoch 4/10, Loss: 2.6997
Epoch 4/10, Loss: 2.5122
Epoch 4/10, Loss: 2.5683
Epoch 4/10, Loss: 2.5306
Epoch 4/10, Loss: 2.5400
Epoch 4/10, Loss: 2.5405
Epoch 4/10, Loss: 2.7225
Epoch 4/10, Loss: 2.5632
Epoch 4/10, Loss: 2.5474
Epoch 4/10, Loss: 2.5998
Epoch 4/10, Loss: 2.4942
Epoch 4/10, Loss: 2.4930
Epoch 4/10, Loss: 2.5663
Epoch 4/10, Loss: 2.5797
Epoch 4/10, Loss: 2.5589
Epoch 4/10, Loss: 2.4884
Epoch 4/10, Loss: 2.5380
Epoch 4/10, Loss: 2.5545
Epoch 4/10, Loss: 2.6295
Epoch 4/10, Loss: 2.6574
Epoch 4/10, Loss: 2.5275
Epoch 4/10, Loss: 2.6040
Epoch 4/10, Loss: 2.6081
Epoch 4/10, Loss: 2.5230
Epoch 4/10, Loss: 2.4683
Epoch 4/10, Loss: 2.6515
Epoch 4/10, Loss: 2.5176
Epoch 4/10, Loss: 2.4425
Epoch 4/10, Loss: 2.5435
Epoch 4/10, Loss: 2.3967
Epoch 4/10, Loss: 2.4716
Epoch 4/10, Loss: 2.6039
Epoch 4/10, Loss: 2.5510
Epoch 4/10, Loss: 2.5517
Epoch 5/10, Loss: 2.4583
Epoch 5/10, Loss: 2.5172
Epoch 5/10, Loss: 2.5392
Epoch 5/10, Loss: 2.6358
Epoch 5/10, Loss: 2.5406
Epoch 5/10, Loss: 2.4847
Epoch 5/10, Loss: 2.4623
Epoch 5/10, Loss: 2.5078
Epoch 5/10, Loss: 2.5984
Epoch 5/10, Loss: 2.6161
Epoch 5/10, Loss: 2.6233
Epoch 5/10, Loss: 2.6159
Epoch 5/10, Loss: 2.5021
Epoch 5/10, Loss: 2.5395
Epoch 5/10, Loss: 2.5462
Epoch 5/10, Loss: 2.5972
Epoch 5/10, Loss: 2.4913
Epoch 5/10, Loss: 2.6598
Epoch 5/10, Loss: 2.5116
Epoch 5/10, Loss: 2.5333
Epoch 5/10, Loss: 2.5086
Epoch 5/10, Loss: 2.5478
Epoch 5/10, Loss: 2.5069
Epoch 5/10, Loss: 2.4893
Epoch 5/10, Loss: 2.4356
Epoch 5/10, Loss: 2.6460
Epoch 5/10, Loss: 2.5658
Epoch 5/10, Loss: 2.7212
Epoch 5/10, Loss: 2.6988
Epoch 5/10, Loss: 2.6791
Epoch 5/10, Loss: 2.5529
Epoch 5/10, Loss: 2.4829
Epoch 5/10, Loss: 2.6514
Epoch 5/10, Loss: 2.6479
Epoch 5/10, Loss: 2.5578
Epoch 5/10, Loss: 2.6055
Epoch 5/10, Loss: 2.5880
Epoch 5/10, Loss: 2.6488
Epoch 5/10, Loss: 2.5024
Epoch 5/10, Loss: 2.5337
Epoch 5/10, Loss: 2.4722
Epoch 5/10, Loss: 2.4675
Epoch 5/10, Loss: 2.3669
Epoch 5/10, Loss: 2.5712
Epoch 5/10, Loss: 2.3895
Epoch 5/10, Loss: 2.5768
Epoch 5/10, Loss: 2.4664
Epoch 5/10, Loss: 2.5032
Epoch 5/10, Loss: 2.5605
Epoch 5/10, Loss: 2.5536
Epoch 5/10, Loss: 2.5543
Epoch 5/10, Loss: 2.5125
Epoch 5/10, Loss: 2.5479
Epoch 5/10, Loss: 2.4986
Epoch 5/10, Loss: 2.5714
Epoch 5/10, Loss: 2.5423
Epoch 5/10, Loss: 2.5495
Epoch 5/10, Loss: 2.5981
Epoch 5/10, Loss: 2.5368
Epoch 5/10, Loss: 2.5486
Epoch 5/10, Loss: 2.5322
Epoch 5/10, Loss: 2.5659
Epoch 6/10, Loss: 2.4679
Epoch 6/10, Loss: 2.6159
Epoch 6/10, Loss: 2.5496
Epoch 6/10, Loss: 2.3818
Epoch 6/10, Loss: 2.5301
Epoch 6/10, Loss: 2.5365
Epoch 6/10, Loss: 2.5327
Epoch 6/10, Loss: 2.5918
Epoch 6/10, Loss: 2.5476
Epoch 6/10, Loss: 2.6458
Epoch 6/10, Loss: 2.5125
Epoch 6/10, Loss: 2.4308
Epoch 6/10, Loss: 2.5310
Epoch 6/10, Loss: 2.4573
Epoch 6/10, Loss: 2.5900
Epoch 6/10, Loss: 2.4894
Epoch 6/10, Loss: 2.6451
Epoch 6/10, Loss: 2.5687
Epoch 6/10, Loss: 2.7178
Epoch 6/10, Loss: 2.5036
Epoch 6/10, Loss: 2.5453
Epoch 6/10, Loss: 2.5491
Epoch 6/10, Loss: 2.5918
Epoch 6/10, Loss: 2.4926
Epoch 6/10, Loss: 2.6068
Epoch 6/10, Loss: 2.6601
Epoch 6/10, Loss: 2.5822
Epoch 6/10, Loss: 2.5609
Epoch 6/10, Loss: 2.5458
Epoch 6/10, Loss: 2.5575
Epoch 6/10, Loss: 2.5252
Epoch 6/10, Loss: 2.5197
Epoch 6/10, Loss: 2.6754
Epoch 6/10, Loss: 2.5616
Epoch 6/10, Loss: 2.5259
Epoch 6/10, Loss: 2.6128
Epoch 6/10, Loss: 2.5466
Epoch 6/10, Loss: 2.6101
Epoch 6/10, Loss: 2.5941
Epoch 6/10, Loss: 2.5503
Epoch 6/10, Loss: 2.5140
Epoch 6/10, Loss: 2.4603
Epoch 6/10, Loss: 2.4868
Epoch 6/10, Loss: 2.6959
Epoch 6/10, Loss: 2.4956
Epoch 6/10, Loss: 2.4824
Epoch 6/10, Loss: 2.6457
Epoch 6/10, Loss: 2.4775
Epoch 6/10, Loss: 2.4811
Epoch 6/10, Loss: 2.6329
Epoch 6/10, Loss: 2.4728
Epoch 6/10, Loss: 2.6474
Epoch 6/10, Loss: 2.5681
Epoch 6/10, Loss: 2.5034
Epoch 6/10, Loss: 2.4706
Epoch 6/10, Loss: 2.4846
Epoch 6/10, Loss: 2.4850
Epoch 6/10, Loss: 2.5339
Epoch 6/10, Loss: 2.5096
Epoch 6/10, Loss: 2.5133
Epoch 6/10, Loss: 2.4590
Epoch 6/10, Loss: 2.3609
Epoch 7/10, Loss: 2.5357
Epoch 7/10, Loss: 2.5421
Epoch 7/10, Loss: 2.6028
Epoch 7/10, Loss: 2.5420
Epoch 7/10, Loss: 2.5254
Epoch 7/10, Loss: 2.4792
Epoch 7/10, Loss: 2.5320
Epoch 7/10, Loss: 2.4778
Epoch 7/10, Loss: 2.5127
Epoch 7/10, Loss: 2.5419
Epoch 7/10, Loss: 2.4963
Epoch 7/10, Loss: 2.3535
Epoch 7/10, Loss: 2.5061
Epoch 7/10, Loss: 2.6903
Epoch 7/10, Loss: 2.4995
Epoch 7/10, Loss: 2.5545
Epoch 7/10, Loss: 2.5458
Epoch 7/10, Loss: 2.7150
Epoch 7/10, Loss: 2.5834
Epoch 7/10, Loss: 2.6465
Epoch 7/10, Loss: 2.6584
Epoch 7/10, Loss: 2.4992
Epoch 7/10, Loss: 2.5530
Epoch 7/10, Loss: 2.6722
Epoch 7/10, Loss: 2.3742
Epoch 7/10, Loss: 2.4696
Epoch 7/10, Loss: 2.4544
Epoch 7/10, Loss: 2.4936
Epoch 7/10, Loss: 2.5922
Epoch 7/10, Loss: 2.4647
Epoch 7/10, Loss: 2.4843
Epoch 7/10, Loss: 2.5572
Epoch 7/10, Loss: 2.6060
Epoch 7/10, Loss: 2.4278
Epoch 7/10, Loss: 2.5364
Epoch 7/10, Loss: 2.6046
Epoch 7/10, Loss: 2.5285
Epoch 7/10, Loss: 2.4594
Epoch 7/10, Loss: 2.5902
Epoch 7/10, Loss: 2.5495
Epoch 7/10, Loss: 2.4546
Epoch 7/10, Loss: 2.4877
Epoch 7/10, Loss: 2.4743
Epoch 7/10, Loss: 2.5181
Epoch 7/10, Loss: 2.5195
Epoch 7/10, Loss: 2.6074
Epoch 7/10, Loss: 2.6317
Epoch 7/10, Loss: 2.4884
Epoch 7/10, Loss: 2.4804
Epoch 7/10, Loss: 2.6011
Epoch 7/10, Loss: 2.5498
Epoch 7/10, Loss: 2.4700
Epoch 7/10, Loss: 2.5631
Epoch 7/10, Loss: 2.5707
Epoch 7/10, Loss: 2.4564
Epoch 7/10, Loss: 2.6437
Epoch 7/10, Loss: 2.6390
Epoch 7/10, Loss: 2.4516
Epoch 7/10, Loss: 2.5945
Epoch 7/10, Loss: 2.4860
Epoch 7/10, Loss: 2.6440
Epoch 7/10, Loss: 2.4519
Epoch 8/10, Loss: 2.4460
Epoch 8/10, Loss: 2.5858
Epoch 8/10, Loss: 2.6045
Epoch 8/10, Loss: 2.6380
Epoch 8/10, Loss: 2.5479
Epoch 8/10, Loss: 2.5599
Epoch 8/10, Loss: 2.6546
Epoch 8/10, Loss: 2.4480
Epoch 8/10, Loss: 2.6015
Epoch 8/10, Loss: 2.4197
Epoch 8/10, Loss: 2.5170
Epoch 8/10, Loss: 2.4750
Epoch 8/10, Loss: 2.3661
Epoch 8/10, Loss: 2.5919
Epoch 8/10, Loss: 2.5398
Epoch 8/10, Loss: 2.5432
Epoch 8/10, Loss: 2.5128
Epoch 8/10, Loss: 2.5316
Epoch 8/10, Loss: 2.5970
Epoch 8/10, Loss: 2.5265
Epoch 8/10, Loss: 2.4837
Epoch 8/10, Loss: 2.5668
Epoch 8/10, Loss: 2.5478
Epoch 8/10, Loss: 2.4780
Epoch 8/10, Loss: 2.5527
Epoch 8/10, Loss: 2.4732
Epoch 8/10, Loss: 2.5387
Epoch 8/10, Loss: 2.5198
Epoch 8/10, Loss: 2.5778
Epoch 8/10, Loss: 2.5335
Epoch 8/10, Loss: 2.4409
Epoch 8/10, Loss: 2.5994
Epoch 8/10, Loss: 2.4899
Epoch 8/10, Loss: 2.4706
Epoch 8/10, Loss: 2.4554
Epoch 8/10, Loss: 2.7146
Epoch 8/10, Loss: 2.4720
Epoch 8/10, Loss: 2.4820
Epoch 8/10, Loss: 2.5395
Epoch 8/10, Loss: 2.4668
Epoch 8/10, Loss: 2.4788
Epoch 8/10, Loss: 2.6903
Epoch 8/10, Loss: 2.3511
Epoch 8/10, Loss: 2.6415
Epoch 8/10, Loss: 2.4368
Epoch 8/10, Loss: 2.4968
Epoch 8/10, Loss: 2.6720
Epoch 8/10, Loss: 2.4457
Epoch 8/10, Loss: 2.5179
Epoch 8/10, Loss: 2.4680
Epoch 8/10, Loss: 2.4313
Epoch 8/10, Loss: 2.5221
Epoch 8/10, Loss: 2.4262
Epoch 8/10, Loss: 2.6282
Epoch 8/10, Loss: 2.6340
Epoch 8/10, Loss: 2.5500
Epoch 8/10, Loss: 2.4617
Epoch 8/10, Loss: 2.4829
Epoch 8/10, Loss: 2.5538
Epoch 8/10, Loss: 2.5939
Epoch 8/10, Loss: 2.5993
Epoch 8/10, Loss: 2.6441
Epoch 9/10, Loss: 2.5102
Epoch 9/10, Loss: 2.5939
Epoch 9/10, Loss: 2.4574
Epoch 9/10, Loss: 2.5180
Epoch 9/10, Loss: 2.5211
Epoch 9/10, Loss: 2.4915
Epoch 9/10, Loss: 2.4657
Epoch 9/10, Loss: 2.6073
Epoch 9/10, Loss: 2.5325
Epoch 9/10, Loss: 2.4675
Epoch 9/10, Loss: 2.4416
Epoch 9/10, Loss: 2.4761
Epoch 9/10, Loss: 2.4532
Epoch 9/10, Loss: 2.6371
Epoch 9/10, Loss: 2.6268
Epoch 9/10, Loss: 2.4202
Epoch 9/10, Loss: 2.3437
Epoch 9/10, Loss: 2.5042
Epoch 9/10, Loss: 2.3582
Epoch 9/10, Loss: 2.5373
Epoch 9/10, Loss: 2.5456
Epoch 9/10, Loss: 2.5553
Epoch 9/10, Loss: 2.6396
Epoch 9/10, Loss: 2.5321
Epoch 9/10, Loss: 2.4150
Epoch 9/10, Loss: 2.4129
Epoch 9/10, Loss: 2.4479
Epoch 9/10, Loss: 2.4780
Epoch 9/10, Loss: 2.6038
Epoch 9/10, Loss: 2.5165
Epoch 9/10, Loss: 2.6707
Epoch 9/10, Loss: 2.5893
Epoch 9/10, Loss: 2.7125
Epoch 9/10, Loss: 2.5952
Epoch 9/10, Loss: 2.5486
Epoch 9/10, Loss: 2.4093
Epoch 9/10, Loss: 2.6533
Epoch 9/10, Loss: 2.4723
Epoch 9/10, Loss: 2.4436
Epoch 9/10, Loss: 2.5463
Epoch 9/10, Loss: 2.4763
Epoch 9/10, Loss: 2.5331
Epoch 9/10, Loss: 2.5903
Epoch 9/10, Loss: 2.6395
Epoch 9/10, Loss: 2.5547
Epoch 9/10, Loss: 2.5682
Epoch 9/10, Loss: 2.5654
Epoch 9/10, Loss: 2.4520
Epoch 9/10, Loss: 2.4057
Epoch 9/10, Loss: 2.4389
Epoch 9/10, Loss: 2.5452
Epoch 9/10, Loss: 2.3994
Epoch 9/10, Loss: 2.6125
Epoch 9/10, Loss: 2.4371
Epoch 9/10, Loss: 2.4684
Epoch 9/10, Loss: 2.6907
Epoch 9/10, Loss: 2.5832
Epoch 9/10, Loss: 2.5371
Epoch 9/10, Loss: 2.5458
Epoch 9/10, Loss: 2.6233
Epoch 9/10, Loss: 2.5196
Epoch 9/10, Loss: 2.4845
Epoch 10/10, Loss: 2.5133
Epoch 10/10, Loss: 2.5421
Epoch 10/10, Loss: 2.3950
Epoch 10/10, Loss: 2.4477
Epoch 10/10, Loss: 2.4340
Epoch 10/10, Loss: 2.4735
Epoch 10/10, Loss: 2.5350
Epoch 10/10, Loss: 2.6077
Epoch 10/10, Loss: 2.4303
Epoch 10/10, Loss: 2.4337
Epoch 10/10, Loss: 2.5466
Epoch 10/10, Loss: 2.4242
Epoch 10/10, Loss: 2.4792
Epoch 10/10, Loss: 2.5107
Epoch 10/10, Loss: 2.4669
Epoch 10/10, Loss: 2.5440
Epoch 10/10, Loss: 2.5109
Epoch 10/10, Loss: 2.6150
Epoch 10/10, Loss: 2.4077
Epoch 10/10, Loss: 2.5322
Epoch 10/10, Loss: 2.7087
Epoch 10/10, Loss: 2.4613
Epoch 10/10, Loss: 2.4207
Epoch 10/10, Loss: 2.5779
Epoch 10/10, Loss: 2.6531
Epoch 10/10, Loss: 2.5636
Epoch 10/10, Loss: 2.6367
Epoch 10/10, Loss: 2.5067
Epoch 10/10, Loss: 2.3495
Epoch 10/10, Loss: 2.6885
Epoch 10/10, Loss: 2.6135
Epoch 10/10, Loss: 2.4950
Epoch 10/10, Loss: 2.6206
Epoch 10/10, Loss: 2.6669
Epoch 10/10, Loss: 2.5899
Epoch 10/10, Loss: 2.3897
Epoch 10/10, Loss: 2.5018
Epoch 10/10, Loss: 2.5416
Epoch 10/10, Loss: 2.4697
Epoch 10/10, Loss: 2.3375
Epoch 10/10, Loss: 2.5395
Epoch 10/10, Loss: 2.6403
Epoch 10/10, Loss: 2.4680
Epoch 10/10, Loss: 2.3836
Epoch 10/10, Loss: 2.4356
Epoch 10/10, Loss: 2.6209
Epoch 10/10, Loss: 2.4891
Epoch 10/10, Loss: 2.4157
Epoch 10/10, Loss: 2.5329
Epoch 10/10, Loss: 2.3779
Epoch 10/10, Loss: 2.5320
Epoch 10/10, Loss: 2.3723
Epoch 10/10, Loss: 2.5848
Epoch 10/10, Loss: 2.5382
Epoch 10/10, Loss: 2.5560
Epoch 10/10, Loss: 2.5638
Epoch 10/10, Loss: 2.5841
Epoch 10/10, Loss: 2.5907
Epoch 10/10, Loss: 2.4779
Epoch 10/10, Loss: 2.4609
Epoch 10/10, Loss: 2.6379
Epoch 10/10, Loss: 2.5513
```

```python
# 获取词向量
# input_embed的权重矩阵形状为(embedding_dim，vocab_size)，比如100*13，13表示13个词，词表的大小，所以某一列就是该词的向量
word_vectors = model.input_embed.weight.T
print(word_vectors.shape)
```

```plaintext
torch.Size([13, 10])
```

```python
for word, idx in vocabulary.items():
    print(f"{word}: {word_vectors[idx]}")
```

```plaintext
I: tensor([ 0.3218,  0.1545, -0.0907, -0.1246,  0.1203, -0.2296,  0.2299, -0.1082,
         0.0174,  0.1791], grad_fn=<SelectBackward0>)
love: tensor([ 0.2430,  0.0880,  0.2220,  0.0109, -0.3393,  0.2886, -0.1101, -0.1124,
        -0.2417, -0.3283], grad_fn=<SelectBackward0>)
natural: tensor([ 0.1837, -0.1624,  0.2591,  0.0044, -0.1978,  0.0886, -0.0188,  0.2499,
        -0.1330,  0.0107], grad_fn=<SelectBackward0>)
language: tensor([ 0.1621, -0.0725, -0.2534, -0.1762, -0.1680, -0.1782, -0.0267,  0.1923,
        -0.0224,  0.1632], grad_fn=<SelectBackward0>)
processing.: tensor([-0.2382, -0.1355,  0.1356, -0.1641, -0.1377, -0.0070,  0.1222,  0.1773,
        -0.2538, -0.2426], grad_fn=<SelectBackward0>)
machine: tensor([ 0.1922, -0.1707,  0.1928,  0.0200, -0.1537,  0.2099, -0.0655, -0.0155,
         0.0618, -0.0274], grad_fn=<SelectBackward0>)
learning.: tensor([ 0.1635, -0.2111, -0.1185,  0.1374,  0.2377, -0.2536,  0.1153, -0.1625,
         0.0216,  0.1828], grad_fn=<SelectBackward0>)
coding: tensor([ 0.2827,  0.2321,  0.1198,  0.0169, -0.3178,  0.0232, -0.1166,  0.1928,
        -0.1159,  0.0610], grad_fn=<SelectBackward0>)
in: tensor([ 0.2521,  0.2306, -0.2162, -0.1707,  0.1203, -0.1165, -0.0119,  0.1528,
        -0.0807, -0.0633], grad_fn=<SelectBackward0>)
Python: tensor([-0.0630,  0.2301,  0.1913, -0.1575,  0.1426, -0.0187, -0.2172,  0.3100,
        -0.0244,  0.0488], grad_fn=<SelectBackward0>)
and: tensor([ 0.1425,  0.1538, -0.1909,  0.0465, -0.1999,  0.1008,  0.2886,  0.1118,
         0.2012,  0.1620], grad_fn=<SelectBackward0>)
Java.: tensor([-0.1860,  0.2746, -0.1024,  0.0957, -0.0056,  0.0860,  0.2734,  0.0683,
         0.0364,  0.0647], grad_fn=<SelectBackward0>)
don't: tensor([-0.0874,  0.0266, -0.2317, -0.0573,  0.1499, -0.2509, -0.0897,  0.1686,
         0.0567, -0.2223], grad_fn=<SelectBackward0>)
```

```python
# 获取某个词的向量
word_vectors[vocabulary['Python']]
```

```plaintext
tensor([-0.0630,  0.2301,  0.1913, -0.1575,  0.1426, -0.0187, -0.2172,  0.3100,
        -0.0244,  0.0488], grad_fn=<SelectBackward0>)
```

```python
import numpy as np

def encode_sentence(sentence):
    vectors = [word_vectors[vocabulary[word]].detach().numpy() for word in sentence.split()]
    print(vectors)
    return np.mean(vectors, axis=0)  # 平均池化

encode_sentence('I love')
```

```plaintext
[array([ 0.32175842,  0.1545292 , -0.0906691 , -0.12461545,  0.12034598,
       -0.22959763,  0.22987527, -0.10824266,  0.01741922,  0.17912774],
      dtype=float32), array([ 0.24295047,  0.08804566,  0.2220389 ,  0.01088865, -0.3392625 ,
        0.2886405 , -0.11014775, -0.11238218, -0.24171409, -0.3283077 ],
      dtype=float32)]





array([ 0.28235444,  0.12128744,  0.0656849 , -0.0568634 , -0.10945825,
        0.02952144,  0.05986376, -0.11031242, -0.11214744, -0.07458998],
      dtype=float32)
```

```python
import torch
import torch.nn as nn

# 使用Embedding层
embedding = nn.Embedding(13, 10)  # 形状是13*10，13表示词的数量，10表示词向量的维度
output_embed = embedding(torch.tensor(2)) # 直接输入词的索引，利用查找表获取词的向量
print(output_embed)

# 打印embedding层的参数值
print(embedding.weight)
```

```plaintext
tensor([-1.0713, -1.0313,  0.5000, -0.7191, -0.3373, -0.1712, -0.9895, -0.4260,
        -0.4475,  0.4031], grad_fn=<EmbeddingBackward0>)
Parameter containing:
tensor([[-0.3864, -0.3228, -0.3692, -1.2301, -1.9629,  0.6103, -1.1924, -0.2367,
          0.0898,  1.5050],
        [ 1.2609,  0.6442,  1.4310,  1.0073,  1.4371, -1.0400,  2.5900, -0.3349,
          0.8031,  0.4660],
        [-1.0713, -1.0313,  0.5000, -0.7191, -0.3373, -0.1712, -0.9895, -0.4260,
         -0.4475,  0.4031],
        [-0.3966, -0.9141,  3.0141, -0.7251,  0.1549,  0.5720,  0.7184, -0.5156,
          1.2174, -0.7913],
        [ 0.2862, -0.5433, -0.2753,  1.3036,  0.8288,  1.4590, -0.1028,  1.2188,
         -0.3152,  0.2742],
        [-1.1940, -1.1333,  0.1844, -0.0668,  0.3242,  1.1618, -0.5508, -0.0779,
          0.1241, -2.5316],
        [-0.2622,  1.8680, -0.2980, -1.0998, -0.0357, -0.1870, -0.2386, -0.0216,
          1.1074,  1.2128],
        [ 0.5118, -1.0450, -1.5705, -2.9756,  0.0277,  2.1754,  0.4007, -0.2478,
         -1.1576,  1.4101],
        [ 0.1469,  2.2284, -1.4061,  0.5307,  1.0168,  0.3197, -0.6883, -0.4878,
         -0.4391,  0.4167],
        [ 0.8928,  0.7945,  1.9765,  0.5093, -0.8774, -0.5338, -0.8494,  1.4396,
          2.0362, -0.6648],
        [-1.0579,  0.4713,  0.3910, -1.1917,  1.1497, -0.4734,  0.8849, -0.0426,
         -1.0717, -0.2240],
        [-0.1127, -0.6535, -1.6889,  0.3810,  0.3663, -0.5219,  0.2627,  1.2062,
         -1.5944, -0.4493],
        [-1.5363, -0.2248,  0.6618,  0.1465, -0.9217,  0.4284,  0.3996,  0.0267,
         -1.5616, -0.7960]], requires_grad=True)
```

```python
import torch
import torch.nn as nn

# 使用Linear层（等效于Embedding + one-hot）
linear = nn.Linear(5, 10, bias=False)  # 形状是5*10
input_one_hot = torch.FloatTensor([0, 0, 1, 0, 0])  # 需要将词的索引转成one-hot向量，然后利用矩阵相乘得到结果
output_linear = linear(input_one_hot)  # 输出形状(1*3)
print(output_linear)
print(linear.weight.T)
```

```plaintext
tensor([ 0.1121, -0.0617,  0.1890,  0.0653, -0.0793, -0.2210,  0.3748,  0.2173,
        -0.2938, -0.2298], grad_fn=<SqueezeBackward4>)
tensor([[-0.2179, -0.1116, -0.3177,  0.1271, -0.3410, -0.3187,  0.3165,  0.4262,
         -0.2732,  0.1637],
        [-0.2948, -0.1186, -0.0515,  0.4112,  0.2941, -0.3868, -0.3594, -0.3256,
         -0.0853, -0.1942],
        [ 0.1121, -0.0617,  0.1890,  0.0653, -0.0793, -0.2210,  0.3748,  0.2173,
         -0.2938, -0.2298],
        [ 0.4214, -0.1592,  0.0412,  0.4196,  0.0868,  0.2042, -0.4394,  0.3085,
          0.1666, -0.0445],
        [ 0.0444, -0.3560,  0.2087,  0.1473,  0.4081, -0.3899, -0.2435,  0.0539,
         -0.2650, -0.2953]], grad_fn=<PermuteBackward0>)
```

这表明在输入为 `one-hot` 编码时，`Embedding` 和 `Linear` 的权重矩阵可以等价，但 `Embedding` 在实现上更为高效。

```python
from torch import nn
from torch import optim

class SkipGram(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.input_embed = nn.Embedding(vocab_size, embedding_dim)
        self.output_embed = nn.Linear(embedding_dim, vocab_size, bias=False)

    def forward(self, center_word):
        hidden = self.input_embed(center_word) # 输入的是词的索引
        return self.output_embed(hidden)


EMBEDDING_DIM = 10

# 初始化模型、损失函数和优化器
model = SkipGram(vocab_size, EMBEDDING_DIM)
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()


# 开始训练
EPOCHS = 100

for epoch in range(EPOCHS):
    for center_batch, target_batch in dataloader:
        predict = model(center_batch)
        loss = criterion(predict, target_batch)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch + 1}/{EPOCHS}, Loss: {loss:.4f}")
```