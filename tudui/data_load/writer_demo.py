from torch.utils.tensorboard import SummaryWriter
import numpy as np
from PIL import Image



writer = SummaryWriter(log_dir="logs")
img_path = "tudui/dataset/hymenoptera_data/train/ants/0013035.jpg"
img_PIL = Image.open(img_path)
img_array = np.array(img_PIL)

writer.add_image("Ant Image", img_array, 0, dataformats='HWC')


writer.close()  