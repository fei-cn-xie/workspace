# 01、Python快速上手

# Python快速上手

## 核心数据类型

```python
print("hello world")
```

```python
# python中变量不需要声明类型

int_val = 42  # 整型

float_val = 3.1415  # 浮点型

is_training = True  # 布尔型

text = "Hello, Zhouyu!"  # 字符串

tuple_val = (16, 768, 123, 1234)  # 元组

list_val = [32, 64, 128, 128]  # 列表 List

set_val = {"CPU", "GPU"}  # Set

dict_val = {"EOS": 50256, "EOS1": 502561}  # 字典 Map Key-Value

print(int_val, float_val, is_training, text, tuple_val, list_val, set_val, dict_val)
```

```python
dict_val.get("EOS1")
```

## 运算符

```python
a = 10

print(a + 3)

print(a - 3)

print(a * 3)

print(a / 3)

print(a % 3)  # 取余数 1

print(a // 3)  # 取整除 商 3

print(a ** 2)  # 平方

print(4 ** 0.5)  # 开平方
```

## 运算符重载

```python
class Custom:
    def __init__(self, value):
        self.value = value

    # 重载 + 运算符
    def __add__(self, other):
        return self.value * other.value

    # # matrix mul
    # def __matmul__(self, other):
    #     return self.value + other.value


a = Custom(3)
b = Custom(4)

c = a @ b
print(c)
```

## 无穷大

在 Python 中，inf（无穷大）和 nan（非数字）是浮点数（float）类型的特殊值，用于处理数学计算中的边界情况

```python
float('inf')
```

```python
pos_inf = float('inf')  # 正无穷

neg_inf = float('-inf')  # 负无穷

print(pos_inf)
print(neg_inf)

print(pos_inf * -1)

print(pos_inf > 10000)
print(neg_inf < -10000)
```

## 非数字nan

```python
import math

a = float('nan')
print(a)

# 比如某个人的年龄是未知的，那么就可以用nan替代
data = [1, 2, float('nan'), 4]
print(data)

cleaned = [x for x in data if not math.isnan(x)]
print(cleaned)
```

## 字符串高级操作

### 字符串格式化

```python
name = "zhouyu"
age = 18

print(f"{name} is {age} years old.")

print("{} is {} years old.".format(name, age))

print("%s is %d years old." % (name, age))
```

### 字符串查找

```python
s = "hello world"

print(s.find("world1"))  # 返回索引 6，找不到返回 -1

print(s.index("world1"))  # 类似 find()，但找不到会报错
```

正则表达式

```python
import re

text = "Python 3.10"
match = re.search(r"\d+\.\d+", text)  # 匹配数字版本
print(match.group())  # 输出 3.10
```

查看python版本

```python
import sys

print(sys.version)
```

### 字符串分割与连接

```python
s = "I love python"

parts = s.split()  # 默认就是按空格切分

print(parts)
```

```python
lines = "line1\nline2\nline3"

print(lines.splitlines())  # ['line1', 'line2', 'line3']
```

```plaintext
['line1', 'line2', 'line3']
```

```python
words = ["I", "love", "python"]

print(" ".join(words))
```

```plaintext
I love python
```

### 字符串对齐与填充

```python
s = "Python"
print(s.ljust(10, "-"))
print(s.rjust(10, "-"))
print(s.center(11, "*"))
```

```plaintext
Python----
----Python
***Python**
```

```python
print("42".zfill(5))
```

```plaintext
00042
```

### 移除空白/特定字符

```python
s = "  python  "
print(s.rstrip())  # "python"
print(s.lstrip())  # "python  "
print(s.strip())
```

```plaintext
  python
python  
python
```

## 列表高级操作

### 切片操作

```python
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(my_list[-1])

print(my_list[2:7])  # 左开右闭区间, 左开右闭（注意：这里反了，应该是左闭右开，闭表示包含）

print(my_list[2:])  # 从索引2开始到末尾

print(my_list[:2])  # 从索引0开始到索引5结束，不包括5，相当于取数组的前5条记录

print(my_list[-2:])  # 获取最后一个元素

print(my_list[1::2])  # 步长为2
```

```plaintext
9
[2, 3, 4, 5, 6]
[2, 3, 4, 5, 6, 7, 8, 9]
[0, 1]
[8, 9]
[1, 3, 5, 7, 9]
```

```python
# 修改切片
my_list[2:5] = [20, 30, 40]
print(my_list)
```

```plaintext
[0, 1, 20, 30, 40, 5, 6, 7, 8, 9]
```

```python
# 删除切片
my_list[2:5] = []
print(my_list)
```

```plaintext
[0, 1, 5, 6, 7, 8, 9]
```

### 列表排序

```python
# 基本排序
numbers = [3, 1, 4, 1, 5, 9, 2]
numbers.sort()
print(numbers)
```

```python
words = ["apple", "banana", "cherry", "date"]
words.sort()
print(words)
```

```plaintext
['apple', 'banana', 'cherry', 'date']
```

```python
# 自定义排序
words = ["apple", "banana", "cherry", "date"]
words.sort(key=len)  # 按长度排序
print(words)
```

```plaintext
['date', 'apple', 'banana', 'cherry']
```

```python
# 多级排序
students = [("Zhouyu", 25), ("Dadudu", 23), ("Xiaodudu", 23)]
students.sort(key=lambda x: (x[1], x[0]))  # 先按年龄，再按姓名
print(students)
```

```plaintext
[('Dadudu', 23), ('Xiaodudu', 23), ('Zhouyu', 25)]
```

```python
# 使用sorted()函数创建新排序列表
original = [3, 1, 4]
new_sorted = sorted(original)
print(original)  # (未改变)
print(new_sorted)
```

```plaintext
[3, 1, 4]
[1, 3, 4]
```

### 列表合并与扩展

```python
# 使用+合并列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]

combined = list1 + list2
print(combined)
print(list1)
print(list2)
```

```plaintext
[1, 2, 3, 4, 5, 6]
[1, 2, 3]
[4, 5, 6]
```

```python
# 使用extend()方法
list1.extend(list2)
print(list1)
print(list2)
```

```plaintext
[1, 2, 3, 4, 5, 6]
[4, 5, 6]
```

```python
# 使用*运算符重复列表
repeated = [0] * 5
print(repeated)
```

```plaintext
[0, 0, 0, 0, 0]
```

### 列表解包(Unpacking)

```python
# 基本解包
first, second, *rest = [1, 2, 3, 4, 5]
print(first)
print(second)
print(rest)
```

```plaintext
1
2
[3, 4, 5]
```

```python
# 忽略某些元素
a, _, b, *rest = [1, 2, 3, 4, 5, 6]
print(a, b, rest)
```

```plaintext
1 3 2 [4, 5, 6]
```

```python
# 嵌套解包
x, (y, z), w = [1, [2, 3], 4]
print(x, y, z, w)  # 1 2 3 4
```

```plaintext
1 2 3 4
```

### 列表推导式（List Comprehension）

```python
# 基本列表推导式
numbers = [x for x in range(10)]
print(numbers)

squares = [x ** 2 for x in range(10)]
print(squares)
```

```plaintext
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

```python
# 带条件的列表推导式
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(even_squares)
```

```plaintext
[0, 4, 16, 36, 64]
```

```python
# 嵌套列表推导式
matrix = [[1, 2, 3], 
          [4, 5, 6], 
          [7, 8, 9]]
result = [num for row in matrix for num in row]
print(result)
```

```plaintext
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 列表与函数式编程

```python
# 使用map函数
numbers = [1, 2, 3, 4]

squared = list(map(lambda x: x ** 2, numbers))
print(squared)
```

```plaintext
[1, 4, 9, 16]
```

```python
# 使用filter函数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)
```

```plaintext
[2, 4]
```

### 列表与数据结构转换

```python
# 列表转字典
keys = ['a', 'b', 'c']
values = [1, 2, 3]

dictionary = dict(zip(keys, values))

print(dictionary)
```

```plaintext
{'a': 1, 'b': 2, 'c': 3}
```

```python
# 列表转集合(去重)
duplicates = [1, 2, 2, 3, 3, 3]
unique = set(duplicates)
print(unique)  # {1, 2, 3}
```

```plaintext
{1, 2, 3}
```

```python
# 列表转字符串
words = ['Hello', 'world']
sentence = ' '.join(words)
print(sentence)  # 'Hello world'
```

```plaintext
Hello world
```

```python
import array

# 创建一个整数数组
my_array = array.array('f', [1, 2, 3, 4, 5])   # 'i' 表示整数
print(my_array)
```

```plaintext
array('f', [1.0, 2.0, 3.0, 4.0, 5.0])
```

### 高级查找与统计

```python
# 使用enumerate获取索引和值
alphas = ['a', 'b', 'c']
for index, value in enumerate(alphas):
    print(index, value)
```

```plaintext
0 a
1 b
2 c
```

```python
# 使用count统计元素出现次数
numbers = [1, 2, 2, 4, 5, 3]
print(numbers.count(2))
```

```plaintext
2
```

```python
# 使用index查找元素位置
print(numbers.index(3))
```

```plaintext
5
```

```python
# 使用any和all函数
print(any(x > 2 for x in numbers))  # 至少有一个元素大于2
print(all(x > 0 for x in numbers))  # 所有元素都大于0
```

```plaintext
True
True
```

## 元组高级操作

元组(tuple)是Python中不可变的序列类型，虽然不如列表灵活，但在某些场景下非常有用

### 元组的不可变性

```python
t = (1, 2, 3, 4)
print(t[0])
t[0] = 10
```

```plaintext
1



---------------------------------------------------------------------------

TypeError                                 Traceback (most recent call last)

Cell In[136], line 3
      1 t = (1, 2, 3, 4)
      2 print(t[0])
----> 3 t[0] = 10


TypeError: 'tuple' object does not support item assignment
```

### 元组解包（Tuple Unpacking）

```python
# 基本解包
a, b, c = (1, 2, 3)
print(a, b, c)  # 输出: 1 2 3
```

```plaintext
1 2 3
```

```python
# 使用*收集剩余元素
first, *middle, last = (1, 2, 3, 4, 5)
print(first)  # 1
print(middle)  # [2, 3, 4] (注意变成了列表)
print(last)  # 5
```

```plaintext
1
[2, 3, 4]
5
```

### 元组作为字典键

```python
# 元组可以作为字典键，而列表不行
locations = {
    (11.1111, 22.2222): "Beijing",
    (55.5555, 66.6666): "Changsha"
}

# locations = {
#     [11.1111, 22.2222]: "Beijing"
# }

print(locations[(11.1111, 22.2222)])
```

```plaintext
Beijing
```

### 元组与函数的配合

```python
# 函数返回多个值实际上是返回元组
def min_max(items):
    return min(items), max(items)


lower, upper = min_max([4, 2, 7, 1, 9])
print(lower, upper)
```

```plaintext
1 9
```

### 元组推导式

```python
# 使用生成器表达式创建元组
t = tuple(x * 2 for x in range(5))
print(t)
```

```plaintext
(0, 2, 4, 6, 8)
```

### 元组与zip函数

```python
names = ('Zhouyu', 'Dadudu', 'Xiaodudu')
scores = (85, 92, 78)

# 压缩之后得到一个元组
combined = tuple(zip(names, scores))
print(combined)

# 压缩之后得到一个list
# combined = list(zip(names, scores))
# print(combined)

# # 压缩之后得到一个dict
# combined = dict(zip(names, scores))
# print(combined)
```

```plaintext
(('Zhouyu', 85), ('Dadudu', 92), ('Xiaodudu', 78))
```

```python
# 解压
names_back = zip(*combined)  # zip('Zhouyu', 'Dadudu', 'Xiaodudu')
print(list(names_back))
# print(scores_back)
```

```plaintext
[('Zhouyu', 'Dadudu', 'Xiaodudu'), (85, 92, 78)]
```

### 元组的内存效率

```python
import sys

# 元组比列表占用更少内存
list_ex = [1, 2, 3]
tuple_ex = (1, 2, 3)

print(sys.getsizeof(list_ex))  # 可能因系统而异
print(sys.getsizeof(tuple_ex))
```

```plaintext
88
64
```

## 字典高级操作

### 字典推导式（Dictionary Comprehension）

```python
# 基本字典推导式
squares = {x: x * 2 for x in range(5)}
print(squares)
```

```plaintext
{0: 0, 1: 2, 2: 4, 3: 6, 4: 8}
```

```python
# 带条件的字典推导式
even_squares = {x: x * 2 for x in range(10) if x % 2 == 0}
print(even_squares)
```

```plaintext
{0: 0, 2: 4, 4: 8, 6: 12, 8: 16}
```

```python
# 从两个列表创建字典
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
print(d)
```

```plaintext
{'a': 1, 'b': 2, 'c': 3}
```

### 合并字典

```python
# 使用 ** 解包
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
merged = {**d1, **d2}  # 后面的字典覆盖前面的
print(d1)
print(d2)
print(merged)
```

```plaintext
{'a': 1, 'b': 2}
{'b': 3, 'c': 4}
{'a': 1, 'b': 3, 'c': 4}
```

```python
# 使用update方法(原地修改)
d1.update(d2)
print(d1)
print(d2)
```

```plaintext
{'a': 1, 'b': 3, 'c': 4}
{'b': 3, 'c': 4}
```

### 字典视图对象

```python
d = {'a': 1, 'b': 2, 'c': 3}

# 获取键、值、键值对视图
keys = d.keys()
values = d.values()
items = d.items()
print(list(keys))
print(list(values))
print(list(items)) # entry
```

```plaintext
['a', 'b', 'c']
[1, 2, 3]
[('a', 1), ('b', 2), ('c', 3)]
```

```python
# 视图是动态的
d['d'] = 4
print(list(keys))
```

```plaintext
['a', 'b', 'c', 'd']
```

### 有序字典(OrderedDict)

```python
from collections import OrderedDict

# 保持插入顺序
od = OrderedDict()
od['a'] = 1
od['c'] = 3
od['b'] = 2
print(list(od.items()))
```

```plaintext
[('a', 1), ('c', 3), ('b', 2)]
```

```python
# 移动元素到最后
od.move_to_end('a')
print(list(od.items()))
```

```plaintext
[('c', 3), ('b', 2), ('a', 1)]
```

```python
# 弹出最后/最前的元素
od.popitem(last=False)  # 移除第一个
print(od)
```

```plaintext
OrderedDict([('b', 2)])
```

### 字典排序

```python
# 按键排序
d = {'b': 2, 'a': 4, 'c': 3}

sorted_by_key = {k: d[k] for k in sorted(d.keys())}
print(sorted_by_key)

# 按值排序
sorted_by_value = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
print(sorted_by_value)

# 多条件排序
d = {'a': 2, 'b': 1, 'c': 2}
sorted_dict = dict(sorted(d.items(), key=lambda x: (x[1], x[0])))
print(sorted_dict)
```

```plaintext
{'a': 4, 'b': 2, 'c': 3}
{'b': 2, 'c': 3, 'a': 4}
{'b': 1, 'a': 2, 'c': 2}
```

## 集合高级操作

### 集合推导式

```python
# 基本集合推导式
squares = {x ** 2 for x in range(5)}
print(squares)

# 带条件的集合推导式
odd_squares = {x ** 2 for x in range(10) if x % 2 != 0}
print(odd_squares)

# 从列表创建集合(去重)
numbers = [1, 2, 2, 3, 3, 3]
unique_numbers = {x for x in numbers}
print(unique_numbers)
```

### 集合运算操作

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 并集
print(a | b)
print(a.union(b))  # 同上
```

```plaintext
{1, 2, 3, 4, 5, 6}
{1, 2, 3, 4, 5, 6}
```

```python
# 交集
print(a & b)
print(a.intersection(b))  # 同上
```

```plaintext
{3, 4}
{3, 4}
```

```python
# 差集
print(a - b)
print(a.difference(b))  # 同上
```

```plaintext
{1, 2}
{1, 2}
```

```python
x = {1, 2, 3}
y = {1, 2}
z = {1, 2, 3, 4}

# 子集判断
print(y <= x)  # y是x的子集
print(y.issubset(x))  # 同上
```

```plaintext
True
True
```

```python
# 超集判断
print(x >= y)  # x是y的超集
print(x.issuperset(y))  # 同上
```

```plaintext
True
True
```

### 集合更新操作

```python
s = {1, 2, 3}

# 添加元素
s.add(4)
print(s)
```

```plaintext
{1, 2, 3, 4}
```

```python
# 添加多个元素
s.update([5, 6], [7, 8])
print(s)
```

```plaintext
{1, 2, 3, 4, 5, 6, 7, 8}
```

```python
# 移除元素
s.discard(8)  # 安全移除，不存在不报错
s.remove(7)  # 移除，不存在会报KeyError
print(s)
```

```plaintext
{1, 2, 3, 4, 5, 6}
```

```python
# 随机弹出元素
popped = s.pop()
print(f"弹出: {popped}, 剩余: {s}")
```

```plaintext
弹出: 3, 剩余: {4, 5, 6}
```

```python
# 清空集合
s.clear()
print(s)  # set()
```

```plaintext
set()
```

### 不可变集合(frozenset)

```python
# 创建不可变集合
fs = frozenset([1, 2, 3, 2])
print(fs)

# 不可变集合可以作为字典键
d = {fs: "123"}
print(d[frozenset([1, 2, 3])])

# 不可变集合支持集合运算但不能修改
fs2 = frozenset([3, 4, 5])
print(fs & fs2)
```

```plaintext
frozenset({1, 2, 3})
123
frozenset({3})
```

### 集合与其它数据结构的转换

```python
# 集合与列表转换
lst = [1, 2, 2, 3]
s = set(lst)
print(s)

back_to_list = list(s)
print(back_to_list)
```

```plaintext
{1, 2, 3}
[1, 2, 3]
```

```python
# 集合与元组转换
t = (1, 2, 2, 3)
s_from_tuple = set(t)
print(s_from_tuple)
```

```plaintext
{1, 2, 3}
```

```python
# 集合与字典转换(只保留键)
d = {'a': 1, 'b': 2}
s_from_dict = set(d)
print(s_from_dict)
```

```plaintext
{'a', 'b'}
```

### 词频统计

```python
text = "this is a sample text with several words and some repeated words"
words = text.split()
print(words)
```

```plaintext
['this', 'is', 'a', 'sample', 'text', 'with', 'several', 'words', 'and', 'some', 'repeated', 'words']
```

```python
unique_words = set(words)
word_count = len(unique_words)
print(f"唯一单词数: {word_count}")
```

```plaintext
唯一单词数: 11
```

## 类与函数

### 定义函数

```python
def greet(name):
    """这是一个简单的问候函数"""
    return f"Hello, {name}!"


# 调用函数
message = greet("Zhouyu")
print(message)
```

```plaintext
Hello, Zhouyu!
```

### 定义类

```python
class Dog:
    # 构造方法、初始化方法
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 实例方法
    def description(self):
        return f"{self.name}现在{self.age}岁"

    # 另一个实例方法
    def speak(self, sound):
        return f"{self.name}说{sound}"


buddy = Dog("旺财", 5)
print(buddy.description())
print(buddy.speak("Hi"))
```

```plaintext
旺财现在5岁
旺财说Hi
```

### 继承

```python
class Bulldog(Dog):  # 继承Dog类
    def run(self, speed):
        return f"{self.name}跑起来很快，速度是{speed}"

# 创建子类实例
jim = Bulldog("大黄", 3)
print(jim.speak("Hello"))  # 继承父类方法
print(jim.run(12))
```

```plaintext
大黄说Hello
大黄跑起来很快，速度是12
```

### 特殊方法

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    # 字符串表示
    def __str__(self):
        return f"{self.title}的作者是{self.author}"

    # 长度
    def __len__(self):
        return self.pages

# 三国演义的作者是
book = Book("三国演义", "罗贯中", 200)
print(book)
print(len(book))
```

```plaintext
三国演义的作者是罗贯中
200
```