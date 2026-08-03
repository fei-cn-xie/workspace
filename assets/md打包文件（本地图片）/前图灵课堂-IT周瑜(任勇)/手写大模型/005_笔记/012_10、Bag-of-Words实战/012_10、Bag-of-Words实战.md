# 10、Bag-of-Words实战

## Bag-of-Words词袋

词袋技术是一种将文本转换为向量的一种方法。

作用：用来将文字表示为向量

特点：忽略词和词之间的顺序，从而忽略了语法、上下文

流程：

1. 先分词，并把词放入“袋子”中，“袋子”中的词是唯一的
2. 再创建词表，给“袋子”中的每个词设置一个编号
3. 依次把文章中的每个句子转成向量，每个句子对应一个向量，向量长度为词表长度，向量的每个位置对应了词表中的每个词，一个句子中有哪些词，就在对应向量中的位置设置为词出现的次数（难理解，看代码容易理解）
4. 最终得到的向量就是句子对应的向量，叫做Bag of Words向量

### 准备语料

```python
# 语料
texts = [
    "I love natural language processing.",
    "I love machine learning.",
    "I love coding in Python and Java.",
    "I love Java.",
    "I love Java, I don't love C++",
    "I don't love Java."
]
```

### 分词

```python
# 分词
words = [word for text in texts for word in text.split()]
print(words)
```

```plaintext
['I', 'love', 'natural', 'language', 'processing.', 'I', 'love', 'machine', 'learning.', 'I', 'love', 'coding', 'in', 'Python', 'and', 'Java.', 'I', 'love', 'Java.', 'I', 'love', 'Java,', 'I', "don't", 'love', 'C++', 'I', "don't", 'love', 'Java.']
```

### 构造词汇表

```python
# 构造词汇表
vocabulary = {}
for word in words:
    if word not in vocabulary:
        vocabulary[word] = len(vocabulary)

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
 'Java,': 12,
 "don't": 13,
 'C++': 14}
```

### 转成bag-of-words向量

```python
# 将原始句子根据词汇表构造为一个向量，称为bag-of-words向量
# 每个向量长度一样，都等于词汇表的长度
# "I love natural language processing.",
bows = []
for text in texts:
    bow = [0] * len(vocabulary)   # 词表长度的全零向量
    for word in text.split():
        bow[vocabulary[word]] += 1
    bows.append(bow)

bows
```

```plaintext
[[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]]
```

"I love Java, I don't love C++",

## 相似度

两个句子的向量相似，就代表两个句子中的词相似，就代表两个句子的语义相似

### 余弦相似度（Cosine Similarity）

- **原理**：计算两个向量的夹角余弦值（忽略向量长度）。
- **公式**：
$cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \cdot \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \cdot \sqrt{\sum_{i=1}^{n} B_i^2}}$
- **应用**：文本相似度、推荐系统

### 点积相似度（Dot Product Similarity）

- **原理**：计算向量的内积（方向 + 长度均考虑）。
- **公式**：
${sim}(\mathbf{A}, \mathbf{B}) = \mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^{n} A_i B_i$
- **应用**：Transformer

```python
# 计算两个向量的相似度
def cosine_similarity(v1, v2):
    dot_product = sum(v1[i] * v2[i] for i in range(len(v1)))
    norm_v1 = sum(v1[i] ** 2 for i in range(len(v1))) ** 0.5
    norm_v2 = sum(v2[i] ** 2 for i in range(len(v2))) ** 0.5
    return dot_product / (norm_v1 * norm_v2)

cosine_similarity([1, 2, 3], [1, 2, 6])
```

```plaintext
0.1984707127330886
```

### 为什么说忽略了向量长度

公式中的$\|\mathbf{A}\|$和$\|\mathbf{B}\|$分别表示向量A和B的模长，向量A除以它的模长，向量B除以它的模长，相当于做了归一化，相当于忽略了向量长度。

```python
# 方向一致，长度相差很大
cosine_similarity([1, 1, 0], [100, 100, 0])
```

```plaintext
0.9999999999999999
```

```python
# 长度一致，方向相差大
cosine_similarity([1, 1, 0], [0, 1, 1])
```

```plaintext
0.4999999999999999
```

### 测试语义相似度

```python
print(texts[2])
print(texts[3])
cosine_similarity(bows[2], bows[3])
```

```plaintext
I love coding in Python and Java.
I love Java.





0.6546536707079772
```

### Bag-of-Words缺点

```python
print(texts[3])
print(texts[5])
cosine_similarity(bows[3], bows[5])
```

```plaintext
I love Java.
I don't love Java.





0.8660254037844387
```

可以看出，"I love Java."和"I don't love Java."语义是完全相反的，但是相似度却很高，这就是词袋模型的缺点。

另外，词汇表越大，那么bow向量也就越长，这也是词袋模型的缺点。