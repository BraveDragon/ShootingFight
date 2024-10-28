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

#ゲームループ本体
def main():
    Game.start(Player1, Player2)
    global Model1P
    global Model2P
    global Target_Model1P
    global Target_Model2P
    global optimizer1P
    global optimizer2P
    global Memory1P
    global Memory2P
    scale = 0.125
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
        Input = convertStateToAgent(State, scale)
        if epsilon > np.random.rand():
            action1P = np.random.randint(0, Agent.Outputs)
            action2P = np.random.randint(0, Agent.Outputs)
        else:
            action1P = Model1P(Input.to(DEVICE)).max()
            action2P = Model2P(Input.to(DEVICE)).max()
            action1P = action1P.cpu().detach().numpy()
            action2P = action2P.cpu().detach().numpy()
        
        NextState, finishedFlag, p1reward, p2reward = Game.update(Player1, Player2, action1P, action2P)
        
        
        if finishedFlag == True:
            current_episode += 1
            # NextStateを「状態なし」に
            NextState = list(NextState)
            NextState[0] = np.full(NextState[0].shape, -1)
            NextState[1] = False
            NextState[2] = False
            NextState = tuple(NextState)
            Target_Model1P.load_state_dict(Model1P.state_dict())
            Target_Model2P.load_state_dict(Model2P.state_dict())
            if step > JustLooking:
                Memory1P.append((State, action1P, p1reward, NextState))
                Memory2P.append((State, action2P, p2reward, NextState))
            step = 0
            Game.start(Player1, Player2)
        else:
            if step > JustLooking:
                Memory1P.append((State, action1P, p1reward, NextState))
                Memory2P.append((State, action2P, p2reward, NextState))
            State = NextState
        if Memory1P.length() > batch_size:
            miniBatch = Memory1P.sample(batch_size)
            targets = torch.empty((batch_size, Agent.Outputs)).to(DEVICE)
            inputs = torch.empty((batch_size, 3, 100, 75)).to(DEVICE)
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                nextState = list(nextState)
                if np.all(nextState[0] == -1) == False:
                    nextState = convertStateToAgent(nextState, scale)
                    with torch.no_grad():
                        maxQ = Target_Model1P(nextState).flatten()
                    target = reward + gamma * torch.max(maxQ)
                else:
                    target = reward
                state = convertStateToAgent(state, scale)
                inputs[i] = state
                targets[i] = Model1P(state).flatten()
                targets[i][action] = target
            optimizer1P.zero_grad()
            outputs = Model1P(inputs)
            loss = criterion1P(outputs, targets)
            loss.backward()
            optimizer1P.step()
        
        if Memory2P.length() > batch_size:
            miniBatch = Memory2P.sample(batch_size)
            targets = torch.empty((batch_size, Agent.Outputs)).to(DEVICE)
            inputs = torch.empty((batch_size, 3, 100, 75)).to(DEVICE)
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                nextState = list(nextState)
                if np.all(nextState[0] == -1) == False:
                    nextState = convertStateToAgent(nextState, scale)
                    with torch.no_grad():
                        maxQ = Target_Model2P(nextState).flatten()
                    target = reward + gamma * torch.max(maxQ)
                else:
                    target = reward
                state = convertStateToAgent(state, scale)
                inputs[i] = state
                targets[i] = Model2P(state).flatten()
                targets[i][action] = target
            optimizer2P.zero_grad()
            outputs = Model2P(inputs)
            loss = criterion2P(outputs, targets)
            loss.backward()
            optimizer2P.step()
                
    SaveModel()

def convertStateToAgent(state : tuple[np.ndarray, int, int], scale = 0.25, device=DEVICE) -> torch.Tensor:
    gameWindow, p1Invincible, p2Invincible = state
    size = (int(Game.Width * scale), int(Game.Height * scale))
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

def SaveModel():
    #モデル+ReplayMemory保存処理
    torch.save(Model1P.state_dict(),"Model1P.pth")
    torch.save(Model2P.state_dict(),"Model2P.pth")

if __name__ == '__main__':
    main()