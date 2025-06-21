

#=nb

import torch
from torch import nn
from torchvision import transforms
from torchvision.transforms import ToTensor, Normalize
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os

path = os.listdir('data')

train_img = np.load(f'data//{path[2]}').reshape(75000, 28,28)
train_lbl = np.load(f'data//{path[3]}')
test_img = np.load(f'data//{path[0]}').reshape(25000 ,28,28)
test_lbl = np.load(f'data//{path[1]}')


transform = transforms.Compose([
    ToTensor(),
    Normalize((0.5), (0.5))
])

class Doodles(Dataset):
    def __init__(self, target, img, transform = None):
        self.target = target
        self.img = img
        self.transform = transform
    def __len__(self):
        return len(self.target)
    def __getitem__(self,idx):
        img = self.img[idx]
        lbl = torch.tensor(self.target[idx]).int()
        if self.transform:
            img = self.transform(img).float()

        return (img, lbl.item())

train_data = Doodles(train_lbl, train_img, transform)
test_data = Doodles(test_lbl, test_img, transform)



test_dataloader = DataLoader(test_data, batch_size = 256, shuffle = True)
train_dataloader = DataLoader(train_data, batch_size = 256, shuffle = True)

divice = ("cuda"
   if torch.cuda.is_available()
   else "mps"
   if torch.backends.mps.is_available()
   else "cpu")


class ConvNet(nn.Module):
  def __init__(self):
    super(ConvNet, self).__init__()
    self.flatten = nn.Flatten()
    self.conv = nn.Sequential(
        nn.Conv2d(1, 32, kernel_size = 3, padding = 1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.Conv2d(32,32, kernel_size = 3, padding = 1),
        nn.ReLU(),
        nn.MaxPool2d(2,2),
        nn.Dropout(0.25),
        nn.Conv2d(32, 64, kernel_size = 3, padding = 1),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        nn.Conv2d(64,64, kernel_size = 3 , padding = 1),
        nn.ReLU()
    )
    self.fc = nn.Sequential(
        nn.Linear(64 * 14 * 14, 256),
        nn.BatchNorm1d(256),
        nn.ReLU(),
        nn.Linear(256, 10)
    )
  def forward(self, x):
    X = self.conv(x)
    X = X.view(-1,64 * 14 * 14)
    X = self.fc(X)
    return X
model = ConvNet().to(divice)


loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3, betas=(0.9, 0.999), eps= 1e-08, weight_decay = 0, amsgrad = False)

def train(model,dataloader, optimizer, loss_fn, print_every = 1):
  model.train()
  size = len(dataloader.dataset)
  for batch, (X,y) in enumerate(dataloader):
    X,y = X.to(divice), y.to(divice)
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if batch % print_every == 0:
      current = (batch + 1) * len(X)
      print(f"loss: {loss.item():.4f},[Current: {current}/{size}]")

def test(model, dataloader, loss_fn, print_every = 1):
  model.eval()
  num_batches = len(dataloader)
  test_loss, correct = 0 , 0
  with torch.no_grad():
    for X,y in dataloader:
      X,y = X.to(divice), y.to(divice)
      pred = model(X)
      test_loss += loss_fn(pred, y).item()
      correct += (pred.argmax(1) == y).type(torch.float).sum().item()
  test_loss /= num_batches
  correct /= len(dataloader.dataset)
  print(f"Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
'''
epoches = 10
for t in range(epoches):
  print(f"Epoch {t+1}\n-------------------------------")
  train(model, train_dataloader, optimizer, loss_fn, print_every = 1000)
  test(model, test_dataloader, loss_fn, print_every = 10)
print("Done!")

torch.save(model.state_dict(), "model.pth")
print("model saved")'''