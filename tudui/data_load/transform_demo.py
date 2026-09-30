from torchvision import transforms
from PIL import Image

img_path = "tudui/dataset/hymenoptera_data/train/ants/0013035.jpg"
img_PIL = Image.open(img_path)
tensor_transform = transforms.ToTensor()
tensor = tensor_transform(img_PIL)
print(f"Tensor shape: {tensor.shape}, Tensor dtype: {tensor.dtype}")
print(tensor)



# 为什么我们需要Tensor的数据类型
# Tensor 需要数据类型，是因为 dtype 决定了：
# 内存怎么解释、精度多高、范围多大、运算结果是什么、能不能用硬件加速、能不能求梯度、能不能和其他系统对接。

from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter(log_dir="logs")

writer.add_image("Ant Image Tensor", tensor, 1)
writer.close()

