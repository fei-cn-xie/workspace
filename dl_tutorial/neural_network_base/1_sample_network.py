import numpy as np

# 将上一级目录（dl_tutorial）加入 Python 搜索路径
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.functions import sigmoid, identity

# 初始化神经网络
# 输入【2】， 第一层【3】，第二层【2】，第三层【2】
def init_network():
    network = {}

    # 第一层参数：输入层到隐藏层
    network["W1"] = np.array([[0.1, 0.2, 0.3], [0.5, 0.4, 0.2]])
    network["b1"] = np.array([1.1, 1.2, 1.3])

    # 第二层参数：输入层到隐藏层 [1,2] -> [0.1]
    network["W2"] = np.array([[0.1, 0.2], [0.5, 0.4], [0.8, 0.7]])
    network["b2"] = np.array([2.2, 2.3])

    # 第三层参数：输入层到隐藏层 [1,2] -> [0.1]
    network["W3"] = np.array([[3.3, 3.3], [3.2, 3.2]])
    network["b3"] = np.array([3.3, 3.4])
    return network


# 前向传播forward 
def forward(net, x):
    w1, w2, w3 = (net[f"W{i}"] for i in range(1, 4))
    b1, b2, b3 = (net[f"b{i}"] for i in range(1, 4))

    # 逐层进行参数传递
    a1 = np.dot(x, w1) + b1
    z1 = sigmoid(a1)

    a2 = np.dot(z1, w2) + b2
    z2 = sigmoid(a2)

    a3 = np.dot(z2, w3) + b3
    y = identity(a3)

    return y

if __name__ == "__main__":

    net = init_network()

    # 定义输入数据
    input = np.array([3, 2])

    # 前向计算
    res = forward(net, input)

    print(f"res = {res}")


