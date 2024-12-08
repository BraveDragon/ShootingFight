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
import Memory
import numpy as np
from collections import deque

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

memsize = 1000
batch_size = 32
gamma = 0.99

Model1P = Agent.Agent().to(DEVICE)
Model2P = Agent.Agent().to(DEVICE)
Target_Model1P = Agent.Agent().to(DEVICE)
Target_Model2P = Agent.Agent().to(DEVICE)
Memory1P = Memory.ReplayMemory(memsize)
Memory2P = Memory.ReplayMemory(memsize)

criterion1P = nn.HuberLoss()
criterion2P = nn.HuberLoss()

optimizer1P = optim.Adam(Model1P.parameters(),lr=0.001,weight_decay=0.005)
optimizer2P = optim.Adam(Model2P.parameters(),lr=0.001,weight_decay=0.005)

max_episode = 10000

#ゲームループ本体
def main():
    Player1 = Player.Player(True)
    Player2 = Player.Player(False)
    Game.start(Player1, Player2)

    global Model1P
    global Model2P
    global Target_Model1P
    global Target_Model2P
    global optimizer1P
    global optimizer2P
    global Memory1P
    global Memory2P
    eps_start = 1.0
    eps_end = 0.01
    eps_reduce_rate = 0.001
    current_episode = 0
    step = 0
    total_step = 0
    input_frames = 4
    window_dim = 3
    InputDeque = deque(maxlen=input_frames)
    InputDeque.extend(np.zeros((input_frames, window_dim, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))
    
    while current_episode < max_episode:
        #最大フレームレートを30fpsで固定
        clock = pygame.time.Clock()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SaveModel()
                pygame.quit()
                sys.exit()
        pygame.display.update()

        epsilon = eps_end + (eps_start - eps_end) * np.exp(-eps_reduce_rate * total_step)
        
        step += 1
        total_step += 1
        State = np.array(InputDeque)
        if epsilon > np.random.rand():
            action1P = np.random.randint(0, Agent.Outputs)
            action2P = np.random.randint(0, Agent.Outputs)
        else:
            Model1P.eval()
            Model2P.eval()
            with torch.no_grad():
                Input = State.reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
                Input = torch.from_numpy(Input).float().to(DEVICE)
                action1P = torch.argmax(Model1P(Input)).cpu().detach().numpy()
                action2P = torch.argmax(Model2P(Input)).cpu().detach().numpy()
        
        NextObservation, finishedFlag, p1reward, p2reward = Game.update(Player1, Player2, action1P, action2P)
        # 1分(30FPS × 60秒 = 1800フレーム)経っても決着が付かない時は両者負けとみなして次のエピソードへ
        if finishedFlag == False and step >= 1800:
            finishedFlag = True
            p1reward = -1
            p2reward = -1
        
        if finishedFlag == True:
            current_episode += 1
            # NextObservationを「状態なし」に
            NextObservation = np.full((window_dim, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)), -1)
            InputDeque.append(NextObservation)
            NextState = np.array(InputDeque)
            Target_Model1P.load_state_dict(Model1P.state_dict())
            Target_Model2P.load_state_dict(Model2P.state_dict())
            
            Memory1P.append((State, action1P, p1reward, NextState))
            Memory2P.append((State, action2P, p2reward, NextState))
            step = 0
            InputDeque.extend(np.zeros((input_frames, window_dim, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))
            Game.start(Player1, Player2)
        else:
            InputDeque.append(Agent.convertStateToAgent(NextObservation, Agent.scale))
            NextState = np.array(InputDeque)
            Memory1P.append((State, action1P, p1reward, NextState))
            Memory2P.append((State, action2P, p2reward, NextState))
            State = NextState
        if Memory1P.length() > batch_size:
            Model1P.train()
            miniBatch = Memory1P.sample(batch_size)
            targets = np.empty((batch_size, Agent.Outputs))
            inputs = np.empty((batch_size, (input_frames * window_dim), int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                if reward == 0:
                    nextState = nextState.reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
                    with torch.no_grad():
                        maxQ = Target_Model1P(torch.from_numpy(nextState).float().to(DEVICE)).flatten()
                    target = (reward + gamma * torch.max(maxQ)).cpu()
                else:
                    target = reward
                inputs[i] = state.reshape((-1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
                targets[i] = Model1P(torch.from_numpy(inputs[i].reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))).float().to(DEVICE)).flatten().detach().cpu().numpy()
                targets[i][action] = target
            optimizer1P.zero_grad()
            outputs = Model1P(torch.from_numpy(inputs).float().to(DEVICE))
            loss = criterion1P(outputs, torch.from_numpy(targets).float().to(DEVICE))
            loss.backward()
            optimizer1P.step()

        if Memory2P.length() > batch_size:
            Model2P.train()
            miniBatch = Memory2P.sample(batch_size)
            targets = np.empty((batch_size, Agent.Outputs))
            inputs = np.empty((batch_size, (input_frames * window_dim), int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                if reward == 0:
                    nextState = nextState.reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
                    with torch.no_grad():
                        maxQ = Target_Model2P(torch.from_numpy(nextState).float().to(DEVICE)).flatten()
                    target = (reward + gamma * torch.max(maxQ)).cpu()
                else:
                    target = reward
                inputs[i] = state.reshape((-1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
                targets[i] = Model2P(torch.from_numpy(inputs[i].reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))).float().to(DEVICE)).flatten().detach().cpu().numpy()
                targets[i][action] = target
            optimizer2P.zero_grad()
            outputs = Model2P(torch.from_numpy(inputs).float().to(DEVICE))
            loss = criterion2P(outputs, torch.from_numpy(targets).float().to(DEVICE))
            loss.backward()
            optimizer2P.step()
                
    SaveModel()



def SaveModel():
    #モデル保存処理
    torch.save(Model1P.state_dict(),"Model1P.pth")
    torch.save(Model2P.state_dict(),"Model2P.pth")

if __name__ == '__main__':
    main()