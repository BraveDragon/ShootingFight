#coding: "utf-8"
import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F
import numpy as np

import Bullet

Inputs = 610
Outputs = 24
#AIを定義するクラス
class Agent(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential( nn.Linear(Inputs,100),
                                   nn.LeakyReLU(),
                                   nn.Linear(100, 50),
                                   nn.LeakyReLU(),
                                   nn.Linear(50, Outputs),
                                   nn.Softmax(dim=0))
    
    def forward(self, x):
        x = self.conv(x)
        return(x)
        

#弾のタイプをOne-Hot形式に変換
def ToOneHotType(bulletlevel:int):
    if bulletlevel == 1:
        return [1, 0, 0]
    elif bulletlevel == 2:
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




