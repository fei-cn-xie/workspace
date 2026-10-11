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
dataset = torchvision.datasets.CIFAR10("tudui/dataset/cifar10", train=False, transform=torchvision.transforms.ToTensor(), download=False)
dataloader = DataLoader(dataset, batch_size=64)


maxpool_demo = MaxPoolDemo()
maxpool_demo = maxpool_demo.to(device) # 新增：将模型参数移动到 GPU

# pip install tensorboard
# tensorboard --logdir=logs
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter(log_dir="logs")
step = 0

for data in dataloader:
    imgs, targets = data
    imgs, targets = imgs.to(device), targets.to(device) # 新增：将数据移动到 GPU
    print(f"imgs.shape = {imgs.shape}")
    output = maxpool_demo(imgs) # 实际调用 nn.Module.__call__
    print(f"output.shape = {output.shape}")

    writer.add_images("MaxpoolDemo - input", imgs, step)
    writer.add_images("MaxpoolDemo - output", output, step)
    step += 1
    