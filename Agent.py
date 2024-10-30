#coding: "utf-8"
#AIのモデルやその関連関数・定数を定義
import torch
import torch.nn as nn
import torch.optim
import numpy as np
import cv2

Outputs = 24
# AIに送信する画面サイズの倍率
scale = 0.125
#デバッグ用の機能を無効化
torch.backends.cudnn.benchmark = True
torch.autograd.set_detect_anomaly(False)
torch.autograd.profiler.emit_nvtx(False)
torch.autograd.profiler.profile(False)

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

def convertStateToAgent(state : tuple[np.ndarray, int, int], device, width, height, scale = 0.25) -> torch.Tensor:
    gameWindow, p1Invincible, p2Invincible = state
    size = (int(width * scale), int(height * scale))
    gameWindow : np.ndarray = cv2.resize(gameWindow.astype(dtype=np.uint8), fx=scale, fy=scale, dsize=None)
    g_min = gameWindow.min()
    g_max = gameWindow.max()
    # 正規化時のゼロ除算対策
    # (g_max - g_min) が0の時(最大値と最小値が同じ時)はg_minが0なら0、そうでないなら1にする
    if (g_max - g_min) == 0:
        gameWindow[:] = 0 if g_min != 0 else 1
    else:
        gameWindow = (gameWindow - g_min) / (g_max - g_min)
    gameWindow = torch.from_numpy(gameWindow).to(device)
    p1Invincible = torch.full(size, int(p1Invincible)).to(device)
    p2Invincible = torch.full(size, int(p2Invincible)).to(device)
    return torch.stack((gameWindow, p1Invincible, p2Invincible)).float()    