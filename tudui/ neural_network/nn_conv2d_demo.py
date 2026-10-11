import torch
import torchvision
from torch import nn

from torch.utils.data import DataLoader

dataset = torchvision.datasets.CIFAR10("tudui/dataset/cifar10", train=True, transform=torchvision.transforms.ToTensor(), download=False)


dataloader = DataLoader(dataset, batch_size=64)


class MyNeuralNetwork(nn.Module):
    def __init__(self):
        super(MyNeuralNetwork, self).__init__()
        # in_channels: 输出图片的通道数-rgb
        # out_channels: 输出图片的通道数
        # kernel_size: 卷积核大小。这里是 3x3 的卷积核。也可以写成 (3, 3)。
        # stride: 卷积核在输入特征图上滑动的步长。这里每次滑动 1 个像素
        # padding: 在输入特征图边缘填充的像素数。这里是 0，表示不填充。
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3, stride=1, padding=0)


    def forward(self, x):
        x = self.conv1(x)
        return x

print("==================Device Info=====================")
# 检查 GPU (ROCm) 是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 可选：打印 GPU 名称，确认是 AMD 显卡
if device.type == 'cuda':
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
print("=================================================")


nn_demo = MyNeuralNetwork()
nn_demo = nn_demo.to(device) # 新增：将模型参数移动到 GPU
print(nn_demo)
# pip install tensorboard
# tensorboard --logdir=logs
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter(log_dir="logs")
step = 0
for data in dataloader:
    imgs, targets = data
    imgs, targets = imgs.to(device), targets.to(device) # 新增：将数据移动到 GPU
    print(f"imgs.shape = {imgs.shape}")
    output = nn_demo(imgs) # 实际调用 nn.Module.__call__
    print(f"output.shape = {output.shape}")
    writer.add_images("input", imgs, step)

    output = torch.reshape(output, (-1, 3, 30, 30)) # torch.Size([16, 6, 30, 30]) -> [xxx, 3, 30, 30]
    # 6个通道转为3个通道， 做了切割，所以64变为128，对应2个图片
    print(f"reshape output = {output.shape}")
    writer.add_images("output", output, step)
    step += 1

