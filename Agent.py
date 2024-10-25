#coding: "utf-8"
import torch
import torch.nn as nn
import torch.optim

Outputs = 23
#この一文で学習を高速化
torch.backends.cudnn.benchmark = True
#AIを定義するクラス
class Agent(nn.Module):
    def __init__(self):
        super().__init__()
        self.rrelu = nn.RReLU()
        self.pool = nn.MaxPool2d(2, stride=2)
        self.conv1 = nn.Conv2d(3, 3, 16)
        self.conv2 = nn.Conv2d(3, 1, 16)
        self.fc1 = nn.Linear(91,32)
        self.fc2 = nn.Linear(32, Outputs)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.rrelu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.rrelu(x)
        x = self.pool(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.rrelu(x)
        x = self.fc2(x)

        return(x)
