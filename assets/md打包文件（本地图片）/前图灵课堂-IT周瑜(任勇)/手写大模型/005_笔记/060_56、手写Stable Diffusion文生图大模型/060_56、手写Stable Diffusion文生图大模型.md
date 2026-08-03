# 56、手写Stable Diffusion文生图大模型

```python
import numpy as np
import torch
from PIL import Image
from torch.optim import AdamW
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 训练数据
dataset = datasets.MNIST(root='./data/', train=True, download=True, transform=transforms.ToTensor())
subset_indices = list(range(1000))
dataloader = DataLoader(dataset, batch_size=64, sampler=torch.utils.data.SubsetRandomSampler(subset_indices))

# 训练参数
T = 1000
betas = torch.linspace(0.0001, 0.02, T)
alphas = 1 - betas
alphas_bar = torch.cumprod(alphas, dim=0)
sqrt_alphas_bar = torch.sqrt(alphas_bar)
sqrt_one_minus_alphas_bar = torch.sqrt(1 - alphas_bar)
```

```python
import os
# 设置环境变量
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"  # 启用高速下载
```

```python
from transformers import ChineseCLIPModel, ChineseCLIPProcessor, AutoTokenizer

clip_model_name = "OFA-Sys/chinese-clip-vit-base-patch16"
clip_model = ChineseCLIPModel.from_pretrained(clip_model_name)
clip_processor = ChineseCLIPProcessor.from_pretrained(clip_model_name)
clip_tokenizer = AutoTokenizer.from_pretrained(clip_model_name)

NUM_TO_TEXT = {
    0: "手写数字0",
    1: "手写数字1",
    2: "手写数字2",
    3: "手写数字3",
    4: "手写数字4",
    5: "手写数字5",
    6: "手写数字6",
    7: "手写数字7",
    8: "手写数字8",
    9: "手写数字9"
}
```

```plaintext
/Users/dadudu/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
Using a slow image processor as `use_fast` is unset and a slow processor was saved with this model. `use_fast=True` will be the default behavior in v4.52, even if the model was saved with a slow processor. This will result in minor differences in outputs. You'll still be able to use a slow processor with `use_fast=False`.
```

```python
from torch.nn import MultiheadAttention
import torch
import torch.nn as nn

class CrossAttention(nn.Module):
    def __init__(self, dim, heads=4):
        super().__init__()
        self.attn = MultiheadAttention(embed_dim=dim, num_heads=heads, batch_first=True)
        self.proj = nn.Linear(dim, dim)
        self.norm = nn.LayerNorm(dim)

    def forward(self, x, context):
        batch_size, channel, height, width = x.shape
        x = x.view(batch_size, channel, -1).permute(0, 2, 1)  # [batch_size, height*width, channel]
        context = context.unsqueeze(1) # [batch_size, context_dim] -> [batch_size, 1, context_dim]
        out, _ = self.attn(x, context, context)  # [batch_size, height*width, channel]
        out = self.norm(out + x) # Add & Norm
        out = self.proj(out)
        out = out.permute(0, 2, 1).view(batch_size, channel, height, width)
        return out

# 两次卷积操作，卷积核为3，填充为1，使得输入和输出的尺寸一致
class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.conv(x)

# 下采样，图片缩小一半
class Down(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Down, self).__init__()
        self.mpconv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_ch, out_ch)
        )

    def forward(self, x):
        return self.mpconv(x)

# 上采样，图片放大两倍
class Up(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Up, self).__init__()
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv = DoubleConv(in_ch, out_ch)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # 裁剪并拼接跳跃连接
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]
        pad_left = diffX // 2
        pad_right = diffX - pad_left
        pad_top = diffY // 2
        pad_bottom = diffY - pad_top
        x1 = nn.functional.pad(x1, [pad_left, pad_right, pad_top, pad_bottom])
        x = torch.cat([x2, x1], dim=1)

        return self.conv(x)

class OutConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(OutConv, self).__init__()
        # 卷积核大小为1，使得输出和输入尺寸一致，但还是变换了图片通道数
        # out_ch=n_classes，n_classes=1，所以就是把之前的图片通道数变为1
        # 最终整个UNet输入一张图片，输出也是一张图片
        self.conv = nn.Conv2d(in_ch, out_ch, 1)

    def forward(self, x):
        # sigmoid是把像素值变为0-1之间
        # return torch.sigmoid(self.conv(x))
        return self.conv(x)

# 大都督周瑜（我的微信: it_zhouyu）

class ZhouyuUNet(nn.Module):
    def __init__(self, n_channels=1, n_classes=1, T=1000, time_emb_dim=64):
        super(ZhouyuUNet, self).__init__()

        self.time_emb = nn.Embedding(T, time_emb_dim)
        self.time_proj = nn.Linear(time_emb_dim, 512)

        self.cross_attn = CrossAttention(dim=512)

        self.inc = DoubleConv(n_channels, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        self.down4 = Down(512, 512)
        self.up1 = Up(512 + 512, 256)   # 通道数：512 (来自下采样) + 512 (上采样输入)
        self.up2 = Up(256 + 256, 128)
        self.up3 = Up(128 + 128, 64)
        self.up4 = Up(64 + 64, 64)
        self.outc = OutConv(64, n_classes)

    def forward(self, x, t, text_emb=None):
        # 时间嵌入
        time_emb = self.time_emb(t)
        time_emb = self.time_proj(time_emb)
        time_emb = time_emb.view(-1, 512, 1, 1)

        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x5 = x5 + time_emb
        x5 = self.cross_attn(x5, text_emb)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.outc(x)
        return x
```

```python
@torch.no_grad()
def encode_texts(texts):
    if isinstance(texts, str):
        texts = [texts]
    tokens = clip_tokenizer(texts, padding=True, return_tensors="pt").to(device)
    text_features = clip_model.get_text_features(**tokens) # [B, 512]
    text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    return text_features
```

```python
model = ZhouyuUNet(T=T, time_emb_dim=64)
optimizer = AdamW(model.parameters(), lr=1e-4)
criterion = nn.MSELoss()

device = "cuda" if torch.cuda.is_available() else "cpu"

clip_model.to(device)
model.to(device)
betas = betas.to(device)
alphas = alphas.to(device)
alphas_bar = alphas_bar.to(device)
sqrt_alphas_bar = sqrt_alphas_bar.to(device)
sqrt_one_minus_alphas_bar = sqrt_one_minus_alphas_bar.to(device)

@torch.no_grad()
def sample(model, text_prompt, num_samples=8):
    model.eval()
    text_emb = encode_texts(text_prompt)  # [1, 512]
    text_emb = text_emb.repeat(num_samples, 1)  # [8, 512]

    x = torch.randn(num_samples, 1, 28, 28).to(device)
    for t in reversed(range(T)):
        t_tensor = torch.full((num_samples,), t, device=device, dtype=torch.long)

        noise_pred = model(x, t_tensor, text_emb=text_emb)

        alpha = alphas[t]
        alpha_bar = alphas_bar[t]
        beta = betas[t]
        z = torch.randn_like(x) if t > 0 else 0

        x = (1 / torch.sqrt(alpha)) * (x - ((1 - alpha) / torch.sqrt(1 - alpha_bar)) * noise_pred) + torch.sqrt(beta) * z

    return x.cpu()

# 训练
os.makedirs("samples", exist_ok=True)
epochs = 300
print("开始训练...")
for epoch in range(epochs):
    model.train()
    total_loss = 0.0
    for step, (images, labels) in enumerate(dataloader):
        batch_size = images.shape[0]
        images = images.to(device)

        # 构造文本描述
        texts = [NUM_TO_TEXT[label.item()] for label in labels]
        text_emb = encode_texts(texts).detach()  # [B, 512]

        # 随机时间步
        t = torch.randint(0, T, (batch_size,), device=device)

        # 加噪声
        sqrt_alpha_bar_t = sqrt_alphas_bar[t].view(-1, 1, 1, 1)
        sqrt_one_minus_alpha_bar_t = sqrt_one_minus_alphas_bar[t].view(-1, 1, 1, 1)
        noise = torch.randn_like(images)
        xt = sqrt_alpha_bar_t * images + sqrt_one_minus_alpha_bar_t * noise

        # 预测噪声（传入文本嵌入）
        noise_pred = model(xt, t, text_emb=text_emb)
        loss = criterion(noise_pred, noise)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")

    # 每 5 个 epoch 采样一次
    if (epoch + 1) % 5 == 0:
        gen_images = sample(model, "手写数字7", num_samples=8)
        gen_images = torch.clamp(gen_images, 0, 1)
        grid = torch.cat([img.squeeze() for img in gen_images], dim=1)
        img = Image.fromarray((grid.numpy() * 255).astype(np.uint8))
        img.save(f"samples/epoch_{epoch+1:03d}.png")
        print(f"Sample saved to samples/epoch_{epoch+1:03d}.png")
```

```plaintext
开始训练...
Epoch [1/300], Loss: 0.5904
Epoch [2/300], Loss: 0.1637



---------------------------------------------------------------------------

KeyboardInterrupt                         Traceback (most recent call last)

Cell In[7], line 66
     63 loss = criterion(noise_pred, noise)
     65 optimizer.zero_grad()
---> 66 loss.backward()
     67 torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
     68 optimizer.step()


File ~/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/_tensor.py:648, in Tensor.backward(self, gradient, retain_graph, create_graph, inputs)
    638 if has_torch_function_unary(self):
    639     return handle_torch_function(
    640         Tensor.backward,
    641         (self,),
   (...)
    646         inputs=inputs,
    647     )
--> 648 torch.autograd.backward(
    649     self, gradient, retain_graph, create_graph, inputs=inputs
    650 )


File ~/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/autograd/__init__.py:353, in backward(tensors, grad_tensors, retain_graph, create_graph, grad_variables, inputs)
    348     retain_graph = create_graph
    350 # The reason we repeat the same comment below is that
    351 # some Python versions print out the first line of a multi-line function
    352 # calls in the traceback and some print out the last line
--> 353 _engine_run_backward(
    354     tensors,
    355     grad_tensors_,
    356     retain_graph,
    357     create_graph,
    358     inputs,
    359     allow_unreachable=True,
    360     accumulate_grad=True,
    361 )


File ~/miniconda3/envs/mini-gpt/lib/python3.10/site-packages/torch/autograd/graph.py:824, in _engine_run_backward(t_outputs, *args, **kwargs)
    822     unregister_hooks = _register_logging_hooks_on_whole_graph(t_outputs)
    823 try:
--> 824     return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
    825         t_outputs, *args, **kwargs
    826     )  # Calls into the C++ engine to run the backward pass
    827 finally:
    828     if attach_logging_hooks:


KeyboardInterrupt: 
```

```python
import matplotlib.pyplot as plt

gen_images = sample(model, "手写数字7", num_samples=8)
gen_images = torch.clamp(gen_images, 0, 1) # 将预测结果的像素值截取到[0, 1]
gen_images = gen_images * 255

fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes = axes.flatten()

for i in range(8):
    img = gen_images[i].squeeze().cpu().numpy()
    axes[i].imshow(img, cmap='gray')
    axes[i].axis("off")

plt.show()
```