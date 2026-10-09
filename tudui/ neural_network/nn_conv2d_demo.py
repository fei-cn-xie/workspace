import torch
import torchvision
from torch import nn

from torch.utils.data import DataLoader

dataset = torchvision.datasets.CIFAR10("tudui/dataset/cifar10", train=True, transform=torchvision.transforms.ToTensor(), download=False)


dataloader = DataLoader(dataset, batch_size=64)


class MyNeuralNetwork(nn.Module):
    def __init__(self):
        super(MyNeuralNetwork, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3, stride=1, padding=0)


    def forward(self, x):
        x = self.conv1(x)
        return x


nn_demo = MyNeuralNetwork()
print(nn_demo)
