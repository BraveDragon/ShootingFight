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
        self.relu = nn.ReLU()
        self.conv1 = nn.Conv2d(12, 8, 1)
        self.conv2 = nn.Conv2d(8, 4, 1)
        self.fc1 = nn.Linear(30000,32)
        self.fc2 = nn.Linear(32, Outputs)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x

def convertStateToAgent(state : np.ndarray, scale = 0.25) -> np.ndarray:
    state : np.ndarray = cv2.resize(state.astype(dtype=np.uint8), fx=scale, fy=scale, dsize=None)
    #cv2.resizeの(幅, 高さ, チャンネル数)形式から(チャンネル数, 幅, 高さ)に変換する
    state = state.transpose((2, 0, 1))
    g_min = state.min()
    g_max = state.max()
    # 正規化時のゼロ除算対策
    # (g_max - g_min) が0の時(最大値と最小値が同じ時)はg_minが0なら0、そうでないなら1にする
    if (g_max - g_min) == 0:
        state[:] = 0 if g_min != 0 else 1
    else:
        state = (state - g_min) / (g_max - g_min)
    
    return state    