# 阶跃函数
def step_function(x):
    if x > 0:
        return 1
    else:
        return 0


import numpy as np

def step_function(x):
    # 将输入 x 与 0 做比较，x > 0 的位置为 True，其余为 False，最后转成整数数组，True/False 分别对应 1/0
    return np.array(x > 0, dtype=int)

# Sigmoid 函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x)) 


# ReLU 函数
def relu(x):
    return np.maximum(0, x)

# softmax 函数
def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)  # 溢出对策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y

# Tanh 函数



if __name__ == '__main__':
    x = np.array([-4.0, -3.0, -2.0, -1.0, 0, 1.0, 2.0, 3.0])
    print(f"x = {x}")
    print("Step 函数 = ", step_function(x))
    print("Sigmoid = ", sigmoid(x))
    print("ReLu = ", relu(x))
    print("Softmax = ", softmax(x), f"sum = {sum(softmax(x))}")