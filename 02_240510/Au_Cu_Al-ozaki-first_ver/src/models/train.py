import os
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from unet import UNet
from pathlib import Path

# Datasetの作成
class CustomDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None):
        self.image_dir = Path(image_dir)
        self.label_dir = Path(label_dir)
        self.file_list = os.listdir(self.image_dir)
        self.transform = transform

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index):
        image_name = os.path.join(self.image_dir, self.file_list[index])
        label_name = os.path.join(self.label_dir, self.file_list[index])

        image = Image.open(image_name)
        label = Image.open(label_name)

        if self.transform:
            image = self.transform(image)
            label = self.transform(label)

        return image, label

# データ拡張
transform = transforms.Compose([
    # transforms.Resize((128, 128)),
    transforms.Grayscale(),
    transforms.ToTensor()
])

image_dir = "./data/interim/images"
label_dir = "./data/interim/labels"
train_dataset = CustomDataset(image_dir=image_dir, label_dir=label_dir, transform=transform)

# Dataloaderの作成
batch_size = 32
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# GPU,モデルの定義
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = UNet().to(device)

# 損失関数,最適化アルゴリズムの定義
criterion = nn.BCEWithLogitsLoss().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# トレーニング
num_epochs = 10
train_losses = []
valid_losses = []

print(f'========== Start Training ==========')

for epoch in range(num_epochs):
    model.train()
    train_loss = 0

    for batch in train_dataloader:
        inputs, labels = batch[0], batch[1]

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
    
    average_train_loss = train_loss / len(train_dataloader)
    train_losses.append(average_train_loss)

# モデルの保存
torch.save(model.state_dict(), "unet_model.pth")


# 学習曲線のプロット
import matplotlib.pyplot as plt

plt.plot(train_losses, label='Train Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


import torchvision.utils as vutils
import os

# ./predフォルダの作成（存在しない場合）
pred_dir = './pred'
if not os.path.exists(pred_dir):
    os.makedirs(pred_dir)

# 1. 検証データセットの準備
valid_image_dir = "./data/raw/images"
valid_label_dir = "./data/raw/labels"
valid_dataset = CustomDataset(image_dir=valid_image_dir, label_dir=valid_label_dir, transform=transform)

# 2. DataLoaderの作成
valid_dataloader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)

# 3. モデルの読み込み
model = UNet().to(device)
model.load_state_dict(torch.load("unet_model.pth"))
model.eval()

# 4. 推論の実行
with torch.no_grad():
    for i, batch in enumerate(valid_dataloader):
        inputs = batch[0].to(device)
        outputs = model(inputs)

        for j in range(outputs.size(0)):
            output = outputs[j].cpu().detach()
            output_img = output.permute(1, 2, 0).numpy()

            # 画像を保存
            save_path = os.path.join(pred_dir, f'pred_{i}_{j}.png')
            vutils.save_image(output, save_path)