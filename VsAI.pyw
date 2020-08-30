#coding: "utf-8"
#プレイヤー VS AI
#ゲーム本体用
import pygame
import sys
import Resources
import Player
import Bullet
#AI用
import Agent
import torch
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
Gunpoint_Speed = 0.6
memsize = 10000
batch_size = 32
JustLooking = 10
current_episode = 0

Player1 = Player.Player(True, False)
Player2 = Player.Player(False,True)

Model2P = Agent.Agent().to(DEVICE)
Model2P.load_state_dict(torch.load("Model2P.pth"))
Model2P.train(False)

with open("memory2P.pkl", "rb") as f:
    Memory2P = pickle.load(f)



#初期化処理
def start():
    global screen
    pygame.init()
    pygame.display.set_caption("ShootingFight")
    screen = pygame.display.set_mode((Width, Height))
    global resource
    resource = Resources.Resources()
    global Player1
    global Player2
    global Bullets
    Bullets = []
    Player1.Reset()
    Player2.Reset()
    


#ゲームの処理
def update():
    #グローバル宣言
    global screen
    global resource
    global Player1
    global Player2
    global Model2P
    global action2P
    global loadaction2P
    global Bullets
    global clock

    #最大フレームレートを60fpsで固定
    clock = pygame.time.Clock()
    clock.tick(60)
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
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == Player1.bulletdirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == Player2.bulletdirection]

    for player1Bullet in player1Bullets:
        for player2Bullet in player2Bullets:
            if getCollition(player1Bullet.x, player2Bullet.x, player1Bullet.y, player2Bullet.y, Bullet.BULLET_RADIUS) == True:
                setWeakening(player1Bullet, player2Bullet)

    Inputs2P = np.array(Memory2P.sample(batch_size), dtype=np.float32)
    action2P = Model2P(torch.from_numpy(Inputs2P).to(DEVICE))
    action2P = np.array(action2P.cpu().detach().numpy())
    loadaction2P = np.argmax(action2P)
    
    State = getState(player1Bullets, player2Bullets)
    #各プレイヤーの動き
    Player1.Move(key, bullets=Bullets)
    Player2.Move(bullets=Bullets,ai_input=action2P)
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1,[Player1.GetX(),Player1.y])
    screen.blit(resource.player2,[Player2.GetX(),Player2.y])

    
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == Player1.bulletdirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == Player2.bulletdirection]

    NextState = getState(player1Bullets, player2Bullets)
    #ReplayMemoryへ保存
    if current_episode > JustLooking:
        Experience2P = []
        Experience2P.extend(State)
        Experience2P.append(float(P2Reward))
        Experience2P.append(loadaction2P)
        Experience2P.extend(NextState)
        Memory2P.load(Experience2P)
    
    State = NextState

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
    global current_episode
    current_episode += 1
    #結果の文字表示
    font = pygame.font.Font(None, 200)
    #1P敗北時
    ret_reward = [0, 0]
    if player1.currentEnergy <= 0:
        ret_reward = [1, -1]
        text = font.render("2P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
    #2P敗北時
    else:
        ret_reward = [-1, 1]
        text = font.render("1P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
    
    if key[pygame.K_SPACE]:
        start()

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
            tpe = Agent.ToOneHotType(player1Bullets[i].bulletlevel)
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
            tpe = Agent.ToOneHotType(player2Bullets[i].bulletlevel)
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
    start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        update()
    

#弾の衝突判定を行う
def getCollition(x1, x2, y1, y2, radius):
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= radius ** 2:
        return True
    else:
        return False

#弾の弱体化を行う
def setWeakening(bullet1P, bullet2P):
    b1afterlevel = bullet1P.bulletlevel - bullet2P.bulletlevel
    b2afterlevel = bullet2P.bulletlevel - bullet1P.bulletlevel
    bullet1P.bulletlevel = b1afterlevel
    bullet2P.bulletlevel = b2afterlevel
    #1Pの弾
    #弾の弱体化+消滅
    if bullet1P.bulletlevel <= 0:
        bullet1P.visible = False
    elif bullet1P.bulletlevel == 1:
        bullet1P.bullettype = Bullet.BULLET_WEAK
    else:
        bullet1P.bullettype = Bullet.BULLET_MIDDLE
    
    #2Pの弾
    #弾の弱体化+消滅
    if bullet2P.bulletlevel <= 0:
        bullet2P.visible = False
    elif bullet2P.bulletlevel == 1:
        bullet2P.bullettype = Bullet.BULLET_WEAK
    else:
        bullet2P.bullettype = Bullet.BULLET_MIDDLE
    

if __name__ == '__main__':
    main()