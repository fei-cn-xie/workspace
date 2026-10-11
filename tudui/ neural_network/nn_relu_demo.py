# 非线性激活
# ReLU = Max(x, 0)

import torch

input = torch.tensor([[1, -0.5],
                      [-1, 3]])

# N = 1：batch size，1 个样本. -1表示这个维度由 PyTorch 自动推断
# C = 1：channel，1 个通道
# H = 2：高度 2
# W = 2：宽度 2
input = torch.reshape(input, (-1, 1, 2,2))

print(input.shape)

from torch import nn
class ReLuDemoNetwork(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relu1 = nn.ReLU(inplace=False)

    def forward(self, input):
        output = self.relu1(input)
        return output



network = ReLuDemoNetwork()
output = network(input)

print(output)