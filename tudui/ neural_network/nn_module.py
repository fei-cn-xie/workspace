import torch
from torch import nn

class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.linear = nn.Linear(2, 1)

    def forward(self, x):
        return self.linear(x)


demo = MyModule()
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
output = demo(x)
print(f"Input: {x}, \nOutput: {output}")
