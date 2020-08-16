#coding: "utf-8"
import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F

import numpy as np
import Bullet

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#AI
Agent = nn.Sequential(
    nn.Linear(244,100),
    nn.LeakyReLU(),
    nn.Linear(100, 50),
    nn.LeakyReLU(),
    nn.Linear(50, 16),
    nn.Softmax()
)

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




