import torch
import torch.nn.functional as F

input = torch.tensor([[1, 2, 0, 3, 1],
                      [0, 1, 2, 3, 1],
                      [1, 2, 1, 0, 0],
                      [5, 2, 3, 1, 1],
                      [2, 1, 0, 1, 1]])

kernel = torch.tensor([[1, 2, 1],
                       [0, 1, 0],
                       [2, 1, 0]])

# (1, 1, 5, 5) -> (batch_size, channels, height, width)
# batch_size: 数据的批次大小，channels: 通道数，height: 高度，width: 宽度
# 通道数是指输入数据的深度，比如彩色图像有3个通道（RGB），灰度图像有1个通道。
# 数据的批次大小是指一次性输入模型的数据量，通常用于加速训练和提高模型的泛化能力。
input = torch.reshape(input, (1, 1, 5, 5))
kernel = torch.reshape(kernel, (1, 1, 3, 3))

output = F.conv2d(input, kernel, stride=1)

print(f"Output shape: {output.shape}, \nOutput: \n{output}")

output1 = F.conv2d(input, kernel, stride=1, padding=1)
print(f"{output1}")