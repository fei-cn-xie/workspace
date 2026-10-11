# 非线性激活
# Sigmoid = 1 / (1 + e^-x)
# 由于ReLU对图片的处理不明显，因此选用sigmoid的激活来演示

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
class SigmoidDemoNetwork(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sigmoid1 = nn.Sigmoid()

    def forward(self, input):
        output = self.sigmoid1(input)
        return output




print("==================Device Info=====================")
# 检查 GPU (ROCm) 是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 可选：打印 GPU 名称，确认是 AMD 显卡
if device.type == 'cuda':
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
print("=================================================")



import torchvision
from torch.utils.data import DataLoader

dataset = torchvision.datasets.CIFAR10("tudui/dataset/cifar10", train=True, transform=torchvision.transforms.ToTensor(), download=False)


dataloader = DataLoader(dataset, batch_size=64)




network = SigmoidDemoNetwork()
network = network.to(device) # 新增：将模型参数移动到 GPU
print(network)
# pip install tensorboard
# tensorboard --logdir=logs
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter(log_dir="logs")
step = 0
for data in dataloader:
    imgs, targets = data
    imgs, targets = imgs.to(device), targets.to(device) # 新增：将数据移动到 GPU
    print(f"imgs.shape = {imgs.shape}")
    output = network(imgs) # 实际调用 nn.Module.__call__
    print(f"output.shape = {output.shape}")
    writer.add_images("Sigmoid Demo = input", imgs, step)

    # output = torch.reshape(output, (-1, 1, 30, 30)) # torch.Size([16, 6, 30, 30]) -> [xxx, 3, 30, 30]
    # # 6个通道转为3个通道， 做了切割，所以64变为128，对应2个图片
    # print(f"reshape output = {output.shape}")
    writer.add_images("Sigmoid Demo = output", output, step)
    step += 1