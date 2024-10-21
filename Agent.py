#coding: "utf-8"
import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F

Inputs = 610
Outputs = 23
#この一文で学習を高速化
torch.backends.cudnn.benchmark = True
#AIを定義するクラス
class Agent(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(Inputs,100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, Outputs)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.rrelu(x)
        x = self.fc2(x)
        x = F.rrelu(x)
        x = self.fc3(x)

        return(x)
        

#弾のタイプをOne-Hot形式に変換
def ToOneHotType(bulletLevel:int):
    if bulletLevel == 1:
        return [1, 0, 0]
    elif bulletLevel == 2:
        return [0, 1, 0]
    else:
        return [0, 0, 1]

#各項目を正規化する
#砲台の位置を正規化
def XNormalize(x:int):
    return x / 600

#弾の位置を正規化
def YNormalize(y:int):
    return y / 600

#エネルギーを正規化
def EnergyNormalize(energy:int):
    return energy / 2000




