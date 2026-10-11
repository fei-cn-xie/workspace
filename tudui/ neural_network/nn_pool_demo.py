# 池化（Pooling），也叫下采样（Subsampling），
# 是卷积神经网络中的一种操作：在特征图上用一个固定大小的窗口按指定步长滑动，
# 对窗口内的元素按某种固定规则进行聚合，得到一个更小的特征图。

# 池化没有真正意义上的“卷积核权重”，更准确的说法是池化窗口（pooling window）。
# 它的 kernel_size、stride、padding 是你自己设定的超参数，但窗口里的计算规则是固定的，不是像卷积那样可以学习或任意自定义每个位置的权重。
# 池化窗口：你只能选择窗口大小、步长、类型（最大/平均），不能给窗口里的每个位置设置不同权重。


import torch
from torch import nn

# max pool

class MaxPoolDemo(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, ceil_mode=True)

    def forward(self, input):
        output = self.maxpool1(input)
        return output

def max_pool_demo():
    input = torch.tensor([[1, 2, 0, 3, 1],
                         [0, 1, 2, 3, 1],
                         [1, 2, 1, 0, 0],
                         [5, 2, 3, 1, 1],
                         [2, 1, 0, 1, 1]])
    input = torch.reshape(input, (-1, 1, 5, 5))
    print(f"input shape = { input.shape}")

    max_pool = MaxPoolDemo()
    output = max_pool(input)

    print(f"output.shape = {output.shape}")
    print(output)


if __name__ == "__main__":
    max_pool_demo()