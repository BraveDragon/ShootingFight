#coding: "utf-8"
#AIをトレーニングする
#ゲーム本体用
import pygame
import sys
import Game
import Player
from Bullet import Bullet
#AI用
import Agent
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import Memory
import pickle

Bullets = []
resource = None
screen = None
clock = None
Player1 = None
Player2 = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
Width = 800
Height = 600

memsize = 10000
batch_size = 32
JustLooking = 10
gamma = 0.99
epsilon = 1.0
eps_end = 0.01
eps_reduce_rate = 0.001
Player1 = Player.Player(True,True)
Player2 = Player.Player(False,True)
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

current_episode = 0
max_episode = 10000

#ゲームの処理
def update():
    #グローバル宣言
    global screen
    global resource
    global Player1
    global Player2
    global Model1P
    global Model2P
    global action1P
    global action2P
    global loadAction1P
    global loadAction2P
    global Target_Model1P
    global Target_Model2P
    global Bullets

    global epsilon
    global eps_end
    #最大フレームレートを60fpsで固定
    clock = pygame.time.Clock()
    clock.tick(60)
    
    if epsilon > eps_end :
        epsilon -= eps_reduce_rate


    #キーボード入力を受け取る
    key = pygame.key.get_pressed()
    #勝敗判定
    if Player1.currentEnergy <= 0 or Player2.currentEnergy <= 0:
       P1reward, P2Reward = Result(Player1, Player2, key, screen)
       #ここでupdate()を打ち切る
       return
    else:
        P1reward = 0
        P2Reward = 0
    
    #画面を黒く塗りつぶす
    screen.fill((0,0,0,0))
    
    if Player1.currentEnergy < Player1.maxEnergy:
        Player1.currentEnergy += 5
    
    if Player2.currentEnergy < Player2.maxEnergy:
        Player2.currentEnergy += 5

    #弾の描画
    for bullet in Bullets:
        bullet.draw(screen,Player1,Player2)

    #画面外に出た弾を消す(実際は画面内にある弾だけ抽出している)
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]

    #弾の衝突判定+弱体化
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == Player1.bulletDirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == Player2.bulletDirection]

    for player1Bullet in player1Bullets:
        for player2Bullet in player2Bullets:
            if Game.getCollision(player1Bullet.x, player2Bullet.x, player1Bullet.y, player2Bullet.y, Bullet.BULLET_RADIUS) == True:
                Game.setWeakening(player1Bullet, player2Bullet)

    if epsilon > np.random.rand():
        raw_action1P = np.random.randint(0, Agent.Outputs)
        raw_action2P = np.random.randint(0, Agent.Outputs)
        action1P = [0] * Agent.Outputs
        action2P = [0] * Agent.Outputs
        action1P[raw_action1P] = 1
        action2P[raw_action2P] = 1
        #ReplayMemoryへの格納用
        loadAction1P = raw_action1P
        loadAction2P = raw_action2P

    elif Memory1P.length() > batch_size and Memory2P.length() > batch_size:
        Inputs1P = np.array(Memory1P.sample(batch_size), dtype=np.float32)
        action1P = Model1P(torch.from_numpy(Inputs1P).to(DEVICE))
        Inputs2P = np.array(Memory2P.sample(batch_size), dtype=np.float32)
        action2P = Model2P(torch.from_numpy(Inputs2P).to(DEVICE))
        action1P = np.array(action1P.cpu().detach().numpy())
        action2P = np.array(action2P.cpu().detach().numpy())
        loadAction1P = np.argmax(action1P)
        loadAction2P = np.argmax(action2P)
    
    State = getState(player1Bullets, player2Bullets)
    #TODO: Reward, action, nextStateの処理

    #各プレイヤーの動き
    Player1.Move(bullets=Bullets,ai_input=action1P)
    Player2.Move(bullets=Bullets,ai_input=action2P)
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1,[Player1.GetX(),Player1.y])
    screen.blit(resource.player2,[Player2.GetX(),Player2.y])

    #ReplayMemoryへ保存
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == Player1.bulletDirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == Player2.bulletDirection]

    NextState = getState(player1Bullets, player2Bullets)

    if current_episode > JustLooking:
        Experience1P = []
        Experience1P.extend(State)
        Experience1P.append(float(P1reward))
        Experience1P.append(loadAction1P)
        Experience1P.extend(NextState)
        Memory1P.load(Experience1P)

        Experience2P = []
        Experience2P.extend(State)
        Experience2P.append(float(P2Reward))
        Experience2P.append(loadAction2P)
        Experience2P.extend(NextState)
        Memory2P.load(Experience2P)
    
    State = NextState
    if Memory1P.length() > batch_size:
        Inputs = np.array(Memory1P.sample(batch_size),dtype=np.float32)
        Output_train = Model1P(torch.from_numpy(Inputs).to(DEVICE))
        Output_Target = Target_Model1P(torch.from_numpy(Inputs).to(DEVICE))
        loss1P = criterion1P(Output_train,Output_Target)
        optimizer1P.zero_grad()
        loss1P.backward(retain_graph=True)
        optimizer1P.step()
    
    if Memory2P.length() > batch_size:
        Inputs = np.array(Memory2P.sample(batch_size),dtype=np.float32)
        Output_train = Model2P(torch.from_numpy(Inputs).to(DEVICE))
        Output_Target = Target_Model2P(torch.from_numpy(Inputs).to(DEVICE))
        loss2P = criterion2P(Output_train,Output_Target)
        optimizer2P.zero_grad()
        loss2P.backward(retain_graph=True)
        optimizer2P.step()



    #エネルギーバーの描画
    #エネルギーの残りで色を変える
    #1P
    if Player1.currentEnergy < 500:
        EnergyColor_1P = (255, 0, 0)
    elif 500 <= Player1.currentEnergy < 1500:
        EnergyColor_1P = (255, 255, 0)
    else:
        EnergyColor_1P = (0, 255, 0)
    
    if Player1.currentEnergy > 0:
        pygame.draw.rect(screen, EnergyColor_1P, [10, 570, Player1.currentEnergy*0.25, 20])
    #2P
    EnergyColor_2P = (0,0,0)
    if Player2.currentEnergy < 500:
        EnergyColor_2P = (255, 0, 0)
    elif 500 <= Player2.currentEnergy < 1500:
        EnergyColor_2P = (255, 255, 0)
    else:
        EnergyColor_2P = (0, 255, 0)
    
    if Player2.currentEnergy > 0:
        pygame.draw.rect(screen, EnergyColor_2P, [290, 10, Player2.currentEnergy*0.25, 20])
    
def Result(player1:Player.Player, player2:Player.Player, key:tuple, surface):
    #結果を反映
    #1P敗北時
    global current_episode
    current_episode += 1
    ret_reward = [0, 0]
    if player1.currentEnergy <= 0:
        ret_reward = [1, -1]
    #2P敗北時
    else:
        ret_reward = [-1, 1]
    
    Game.start(player1, player2)
    return ret_reward

def getState(player1Bullets, player2Bullets):
    #状態の取得
    P1x = Agent.XNormalize(Player1.GetX())
    P2x = Agent.XNormalize(Player2.GetX())
    P1Energy = Agent.EnergyNormalize(Player1.currentEnergy)
    P2Energy = Agent.EnergyNormalize(Player2.currentEnergy)
    P1bullets = []
    P2bullets = []
    for i in range(30):
        if i < len(player1Bullets):
            x = Agent.XNormalize(player1Bullets[i].x)
            y = Agent.YNormalize(player1Bullets[i].y)
            tpe = Agent.ToOneHotType(player1Bullets[i].bulletLevel)
        else:
            x = -1
            y = -1
            tpe = [0,0,0]
            pass
        
        P1bullets.append(x)
        P1bullets.append(y)
        P1bullets.extend(tpe)    
    
    for i in range(30):
        if i < len(player2Bullets):
            x = Agent.XNormalize(player2Bullets[i].x)
            y = Agent.YNormalize(player2Bullets[i].y)
            tpe = Agent.ToOneHotType(player2Bullets[i].bulletLevel)
        else:
            x = -1
            y = -1
            tpe = [0,0,0]
            pass
        
        P2bullets.append(x)
        P2bullets.append(y)
        P2bullets.extend(tpe)

    State = []
    State.append(P1x)
    State.append(P2x)
    State.append(P1Energy)
    State.append(P2Energy)
    State.extend(P1bullets)
    State.extend(P2bullets)

    return State


#ゲームループ本体
def main():
    Game.start()
    #楽観的初期化を行う
    global Target_Model1P
    global Target_Model2P
    global optimizer1P
    global optimizer2P
    #何回か楽観的初期化を回す
    IsNeeded_retain = True
    for _ in range(10):
        x1 = Target_Model1P(torch.ones(Agent.Inputs).to(DEVICE))
        x2 = Target_Model2P(torch.ones(Agent.Inputs).to(DEVICE))
        out1P = torch.ones(Agent.Outputs).to(DEVICE)
        out2P = torch.ones(Agent.Outputs).to(DEVICE)
        loss1P = criterion1P(out1P,x1)
        loss2P = criterion2P(out2P,x2)
        optimizer1P.zero_grad()
        optimizer2P.zero_grad()
        loss1P.backward(retain_graph=IsNeeded_retain)
        loss2P.backward(retain_graph=IsNeeded_retain)
        IsNeeded_retain = False
        optimizer1P.step()
        optimizer2P.step()
    
    while current_episode < max_episode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SaveModel()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        update()
    
    SaveModel()

def SaveModel():
    #モデル+ReplayMemory保存処理
    torch.save(Model1P.state_dict(),"Model1P.pth")
    torch.save(Model2P.state_dict(),"Model2P.pth")

    with open("memory1P.pkl", "wb") as memory:
        pickle.dump(Memory1P, memory)

    with open("memory2P.pkl", "wb") as memory:
        pickle.dump(Memory2P, memory)

if __name__ == '__main__':
    main()