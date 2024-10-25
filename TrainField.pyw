#coding: "utf-8"
#AIをトレーニングする
import pygame
import sys
import Game
import Player
#AI用
import Agent
import torch
import torch.optim as optim
import torch.nn as nn
import cv2
import Memory
import numpy as np

Bullets = []
Player1 = None
Player2 = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

memsize = 10000
batch_size = 32
JustLooking = 10
gamma = 0.99

Player1 = Player.Player(True)
Player2 = Player.Player(False)
Model1P = Agent.Agent().to(DEVICE)
Model2P = Agent.Agent().to(DEVICE)
Target_Model1P = Agent.Agent().to(DEVICE)
Target_Model2P = Agent.Agent().to(DEVICE)
Memory1P = Memory.ReplayMemory(memsize)
Memory2P = Memory.ReplayMemory(memsize)

Model1P.train(True)
Model2P.train(True)
Target_Model1P.train(True)
Target_Model2P.train(True)
criterion1P = nn.SmoothL1Loss()
criterion2P = nn.SmoothL1Loss()

optimizer1P = optim.Adam(Model1P.parameters(),lr=0.001,weight_decay=0.005)
optimizer2P = optim.Adam(Model2P.parameters(),lr=0.001,weight_decay=0.005)

max_episode = 10000

#     if current_episode > JustLooking:
#         Experience1P = []
#         Experience1P.extend(State)
#         Experience1P.append(float(P1reward))
#         Experience1P.append(loadAction1P)
#         Experience1P.extend(NextState)
#         Memory1P.append(Experience1P)

#         Experience2P = []
#         Experience2P.extend(State)
#         Experience2P.append(float(P2Reward))
#         Experience2P.append(loadAction2P)
#         Experience2P.extend(NextState)
#         Memory2P.append(Experience2P)
    
#     State = NextState
#     if Memory1P.length() > batch_size:
#         Inputs = np.array(Memory1P.sample(batch_size),dtype=np.float32)
#         Output_train = Model1P(torch.from_numpy(Inputs).to(DEVICE))
#         Output_Target = Target_Model1P(torch.from_numpy(Inputs).to(DEVICE))
#         loss1P = criterion1P(Output_train,Output_Target)
#         optimizer1P.zero_grad()
#         loss1P.backward(retain_graph=True)
#         optimizer1P.step()
    
#     if Memory2P.length() > batch_size:
#         Inputs = np.array(Memory2P.sample(batch_size),dtype=np.float32)
#         Output_train = Model2P(torch.from_numpy(Inputs).to(DEVICE))
#         Output_Target = Target_Model2P(torch.from_numpy(Inputs).to(DEVICE))
#         loss2P = criterion2P(Output_train,Output_Target)
#         optimizer2P.zero_grad()
#         loss2P.backward(retain_graph=True)
#         optimizer2P.step()

#ゲームループ本体
def main():
    Game.start(Player1, Player2)
    global Target_Model1P
    global Target_Model2P
    global optimizer1P
    global optimizer2P
    global Memory1P
    global Memory2P
    epsilon = 1.0
    eps_end = 0.01
    eps_reduce_rate = 0.001
    current_episode = 0
    step = 0
    
    while current_episode < max_episode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SaveModel()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if epsilon > eps_end:
            epsilon -= eps_reduce_rate
        
        action1P = -1
        action2P = -1
        step += 1
        State, finishedFlag, _, _ = Game.getObservation(Player1, Player2)
        gameWindow, p1Invincible, p2Invincible = State
        scale = 0.125
        gameWindow = cv2.resize(np.array(gameWindow, dtype='uint8'), fx=scale, fy=scale, dsize=None)
        g_min = gameWindow.min()
        g_max = gameWindow.max()
        # 正規化時のゼロ除算対策
        # (g_max - g_min) が0の時(最大値と最小値が同じ時)はg_minに置き換える
        if (g_max - g_min) == 0:
            gameWindow[:] = g_min
        else:
            gameWindow = (gameWindow - g_min) / (g_max - g_min)
        p1Invincible = torch.full((int(Game.Width * scale), int(Game.Height * scale)),int(p1Invincible))
        p2Invincible = torch.full((int(Game.Width * scale), int(Game.Height * scale)), int(p2Invincible))
        State = torch.from_numpy(np.array((gameWindow, p1Invincible, p2Invincible))).to(DEVICE)
        if epsilon > np.random.rand():
            action1P = np.random.randint(0, Agent.Outputs)
            action2P = np.random.randint(0, Agent.Outputs)
        else:
            action1P = Model1P(State.float())
            action2P = Model2P(State.float())
            action1P = np.array(action1P.cpu().detach().numpy()).argmax()
            action2P = np.array(action2P.cpu().detach().numpy()).argmax()
        
        NextState, finishedFlag, p1reward, p2reward = Game.update(Player1, Player2, action1P, action2P)
        
        
        if finishedFlag == True:
            current_episode += 1
            # NextStateを「状態なし」に
            NextState = list(NextState)
            NextState[0] = np.zeros(NextState[0].shape)
            NextState[1] = False
            NextState[2] = False
            NextState = tuple(NextState)
            if step > JustLooking:
                Memory1P.append((State, action1P, p1reward, NextState))
                Memory2P.append((State, action2P, p2reward, NextState))
            step = 0
            Game.start(Player1, Player2)
        else:
            State = NextState
    
    SaveModel()

def SaveModel():
    #モデル+ReplayMemory保存処理
    torch.save(Model1P.state_dict(),"Model1P.pth")
    torch.save(Model2P.state_dict(),"Model2P.pth")

if __name__ == '__main__':
    main()