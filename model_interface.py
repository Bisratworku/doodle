import torch
import torch.nn as nn
from torchvision.transforms import transforms
import json
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image

divice = ("cuda"
   if torch.cuda.is_available()
   else "mps"
   if torch.backends.mps.is_available()
   else "cpu")
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
class ConvNet(nn.Module):
  def __init__(self):
    super(ConvNet, self).__init__()
    self.flatten = nn.Flatten()
    self.conv = nn.Sequential(
        nn.Conv2d(1, 32, kernel_size= 3, padding = 1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size = 2, stride = 2 , padding = 1),
        nn.Conv2d(32, 64, kernel_size= 3, padding = 1 ),
        nn.MaxPool2d(kernel_size = 2, stride = 2 , padding = 1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size= 2),
        nn.Conv2d(64, 64, kernel_size= 3, padding = 1 ),
        nn.ReLU(),
    )
    self.fc = nn.Sequential(
            nn.Linear(1024, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
    )
  def forward(self, x):
    X = self.conv(x)
    X = self.flatten(X)
    X = self.fc(X)
    return X
class model():
  def __init__(self):      
    self.model = ConvNet().to(divice)
    self.model.load_state_dict(torch.load("C:\\Users\\pro\\Documents\\GitHub\\doodle\\train\\model.pth"))
    self.classes = {
        0: "airpalne",
        1 : "alarm",
        2 : "ant",
        3 : "apple",
        4 : "arm",
        5 : "axe",
        6 : "bat",
        7 : "bed",
        8 : "birthday_cake",
        9 : "camera"
    }
  def predict(self):
    self.path = "C:\\Users\\pro\\Documents\\GitHub\\doodle\\img.json"
    with open(self.path, 'r')as f:
        data = json.load(f)
    img = np.array(data['data'], dtype = np.uint8)
    image = Image.fromarray(img)
    image = image.resize((28,28))
    image = transform(image)
    image = image.reshape(1,1,28,28)
    return self.classes[self.model(image).argmax(1).item()]