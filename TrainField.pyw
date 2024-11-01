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

memsize = 10000
batch_size = 32
JustLooking = 10
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
    InputDeque = deque(maxlen=input_frames)
    for _ in range(input_frames):
        InputDeque.append(np.zeros((int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))
    
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
        State, finishedFlag, _, _ = Game.getObservation(Player1, Player2)
        InputDeque.append(Agent.convertStateToAgent(State, Agent.scale))
        if epsilon > np.random.rand():
            action1P = np.random.randint(0, Agent.Outputs)
            action2P = np.random.randint(0, Agent.Outputs)
        else:
            Model1P.eval()
            Model2P.eval()
            with torch.no_grad():
                Input = torch.from_numpy(np.array(InputDeque)).float().to(DEVICE)
                action1P = torch.argmax(Model1P(Input)).argmax().cpu().detach().numpy()
                action2P = torch.argmax(Model2P(Input)).argmax().cpu().detach().numpy()
        
        NextState, finishedFlag, p1reward, p2reward = Game.update(Player1, Player2, action1P, action2P)
        
        if finishedFlag == True:
            current_episode += 1
            # NextStateを「状態なし」に
            NextState = np.full((int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)), -1)
            
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
            Model1P.train()
            miniBatch = Memory1P.sample(batch_size)
            targets = np.empty((batch_size, Agent.Outputs))
            inputs = np.empty((batch_size, 4, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                if np.all(nextState == -1) == False:
                    nextState = Agent.convertStateToAgent(State, Agent.scale)
                    InputDeque.append(nextState)
                    nextState = np.array(InputDeque)
                    with torch.no_grad():
                        maxQ = Target_Model1P(torch.from_numpy(nextState).float().to(DEVICE)).flatten()
                    target = (reward + gamma * torch.max(maxQ)).cpu()
                else:
                    target = reward
                state = Agent.convertStateToAgent(State, Agent.scale)
                InputDeque.append(state)
                inputs[i] = np.array(InputDeque)
                targets[i] = Model1P(torch.from_numpy(inputs[i]).float().to(DEVICE)).flatten().detach().cpu().numpy()
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
            inputs = np.empty((batch_size, 4, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
            for i, (state, action, reward, nextState) in enumerate(miniBatch):
                if np.all(nextState == -1) == False:
                    nextState = Agent.convertStateToAgent(State, Agent.scale)
                    InputDeque.append(nextState)
                    nextState = np.array(InputDeque)
                    with torch.no_grad():
                        maxQ = Target_Model2P(torch.from_numpy(nextState).float().to(DEVICE)).flatten()
                    target = (reward + gamma * torch.max(maxQ)).cpu()
                else:
                    target = reward
                state = Agent.convertStateToAgent(State, Agent.scale)
                InputDeque.append(state)
                inputs[i] = np.array(InputDeque)
                targets[i] = Model2P(torch.from_numpy(inputs[i]).float().to(DEVICE)).flatten().detach().cpu().numpy()
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