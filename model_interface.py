import torch
import torch.nn as nn
import json
import matplotlib.pyplot as plt

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
    '''
    zeros = torch.zeros(1,1,28,28)
    output = self.conv(zeros)
    print(self.flatten(output).shape)'''
    self.fc = nn.Sequential(
        nn.Linear(12544, 256),
        nn.ReLU(),
        nn.Linear(256, 500),
        nn.ReLU(),
        nn.Linear(500, 10)
    )
  def forward(self, x):
    X = self.conv(x)
    X = self.flatten(X)
    X = self.fc(X)
    return X

class recognaize():
    def __init__(self):
        with open('img.json') as f:
           self.data = json.load(f)
    def reshape_resize(self):
        img = torch.tensor(self.data['data']).reshape(self.data['height'], self.data['width'], 4).float().sum(-1)
        pool = nn.AdaptiveAvgPool2d((28,28))
        output = pool(img.reshape(1,1,300,300)) # 300 is the height and the width of the image this could easly be repalced with self.data['height'] or self.data['width']
        return output
    def pridict(self):
        model = ConvNet().to(divice)
        model.load_state_dict(torch.load('train//model.pth'))
        pred = model(self.reshape_resize())
        return pred.argmax(1).item()