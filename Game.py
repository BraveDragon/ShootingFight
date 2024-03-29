#coding: "utf-8"
#ゲーム本体用
import pygame
import sys
import Objects
import Resources
import Bullet
import Player
import numpy as np


Bullets = []
UFOs = []
Aliens = []
resource = None
screen = None
clock = None

Width = 800
Height = 600
Gunpoint_Speed = 0.6

MAX_UFOs = 1
MAX_Aliens = 2

#初期化処理
def start(player1:Player.Player, player2:Player.Player):
    global screen
    pygame.init()
    pygame.display.set_caption("ShootingFight")
    screen = pygame.display.set_mode((Width, Height))
    
    global resource
    resource = Resources.Resources()
    global Bullets
    global UFOs
    global Aliens
    
    Bullets = []
    UFOs = []
    Aliens = []
    player1.Reset()
    player2.Reset()
    


#ゲームの処理
def update(player1:Player.Player, player2:Player.Player, P1Input:int=-1, P2Input:int=-1):
    #グローバル宣言
    global screen
    global resource
    global Bullets
    global UFOs
    global Aliens
    #最大フレームレートを60fpsで固定
    clock = pygame.time.Clock()
    clock.tick(60)

    #キーボード入力を受け取る
    key = pygame.key.get_pressed()
    #勝敗判定
    if player1.currentEnergy <= 0 or player2.currentEnergy <= 0:
        P1reward, P2reward = Result(player1,player2, key, screen)
        #ここでupdate()を打ち切る
        return (pygame.surfarray.array3d(pygame.display.get_surface()),P1reward,P2reward)
    
    #画面を黒く塗りつぶす
    screen.fill((0,0,0,0))
    
    if player1.currentEnergy < Player.Player.maxEnergy:
        player1.currentEnergy += 5
    
    if player2.currentEnergy < Player.Player.maxEnergy:
        player2.currentEnergy += 5
    

    #弾の描画
    for bullet in Bullets:
        bullet.draw(screen,player1,player2)

    #画面外に出た弾を消す(実際は画面内にある弾だけ抽出している)
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]

    #弾の衝突判定+弱体化
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == player1.bulletdirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletdirection == player2.bulletdirection]

    for player1Bullet in player1Bullets:
        for player2Bullet in player2Bullets:
            if getCollision(player1Bullet.x, player2Bullet.x, player1Bullet.y, player2Bullet.y, Bullet.BULLET_RADIUS, Bullet.BULLET_RADIUS) == True:
                setWeakening(player1Bullet, player2Bullet)
    
    #弾とエイリアンの衝突判定
    for bullet in Bullets:
        for alien in Aliens:
            if getCollision(bullet.x, alien.x, bullet.y, alien.y, Bullet.BULLET_RADIUS, alien.radius) == True:
                collisionAlien(bullet,alien,player1,player2)
    
    #エイリアンに当たった弾を削除
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]
    #弾に当たったエイリアンを削除
    Aliens = [alien for alien in Aliens if alien.visible == True]

    #弾とUFOの衝突判定
    for bullet in Bullets:
        for ufo in UFOs:
            if getCollision(bullet.x, ufo.x, bullet.y, ufo.y, Bullet.BULLET_RADIUS, ufo.radius) == True:
                collisionUFO(bullet,alien,player1,player2)
    
    #UFOに当たった弾を削除
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]
    #弾に当たったエイリアンを削除
    UFOs = [ufo for ufo in UFOs if ufo.visible == True]

    #各プレイヤーの動き
    player1.Move(key=key,bullets=Bullets,ai_input=P1Input)
    player2.Move(key=key,bullets=Bullets,ai_input=P2Input)
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1,[player1.GetX(),player1.y])
    screen.blit(resource.player2,[player2.GetX(),player2.y])
    #エイリアンの生成
    if len(Aliens) <= MAX_Aliens:
        x = np.random.rand() * (Width / 2)
        y = np.random.rand() * (Height * 0.5) + 100
        LorR = np.random.rand()
        if LorR > 0.5:
            Aliens.append(Objects.Objects(x,y,Objects.ALIEN,moveToRightFlag=True))
        else:
            Aliens.append(Objects.Objects(x,y,Objects.ALIEN,moveToRightFlag=False))
    #エイリアンの描画
    for alien in Aliens:
        alien.draw(screen,resource.alien)
    #画面外に出たエイリアンを削除
    Aliens = [alien for alien in Aliens if alien.visible == True]
    
    #UFOの生成
    if len(UFOs) <= MAX_UFOs:
        x = np.random.rand() * (Width / 2)
        y = np.random.rand() * (Height * 0.5) + 100
        LorR = np.random.rand()
        if LorR > 0.5:
            UFOs.append(Objects.Objects(x,y,Objects.UFO,moveToRightFlag=True))
        else:
            UFOs.append(Objects.Objects(x,y,Objects.UFO,moveToRightFlag=False))
    for ufo in UFOs:
        ufo.draw(screen,resource.ufo)
    #画面外に出たUFOを削除
    UFOs = [ufo for ufo in UFOs if ufo.visible == True]

    #無敵状態の処理
    if player1.IsInvincible == True:
        player1.InvincibleCount += 1
    if player1.IsInvincible == True and player1.InvincibleCount >= Player.InvincibleTime:
        player1.IsInvincible = False
        player1.InvincibleCount = 0
    
    if player2.IsInvincible == True:
        player2.InvincibleCount += 1
    if player2.IsInvincible == True and player2.InvincibleCount >= Player.InvincibleTime:
        player2.IsInvincible = False
        player2.InvincibleCount = 0
    
    #エネルギーバーの描画
    #エネルギーの残りで色を変える
    #無敵状態の時は残りエネルギーに関わらず青色になる
    #1P
    if player1.IsInvincible == True:
        EnergyColor_1P = (0, 0, 255)
    elif player1.currentEnergy < 500:
        EnergyColor_1P = (255, 0, 0)
    elif 500 <= player1.currentEnergy < 1500:
        EnergyColor_1P = (255, 255, 0)
    else:
        EnergyColor_1P = (0, 255, 0)
    
    if player1.currentEnergy > 0:
        pygame.draw.rect(screen, EnergyColor_1P, [10, 570, int(player1.currentEnergy*0.25), 20])
    #2P
    if player2.IsInvincible == True:
        EnergyColor_2P = (0, 0, 255)
    elif player2.currentEnergy < 500:
        EnergyColor_2P = (255, 0, 0)
    elif 500 <= player2.currentEnergy < 1500:
        EnergyColor_2P = (255, 255, 0)
    else:
        EnergyColor_2P = (0, 255, 0)
    
    if player2.currentEnergy > 0:
        pygame.draw.rect(screen, EnergyColor_2P, [290, 10, int(player2.currentEnergy*0.25), 20])
    
    return (pygame.surfarray.array3d(pygame.display.get_surface()), 0, 0)
    
    

    
def Result(player1:Player.Player,player2:Player.Player, key:tuple, surface):
    #結果の文字表示
    font = pygame.font.Font(None, 200)
    if key[pygame.K_SPACE]:
        start(player1, player2)
    #1P敗北時
    if player1.currentEnergy <= 0:
        text = font.render("2P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
        return (-1, 1)
    #2P敗北時
    else:
        text = font.render("1P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
        return (1, -1)

#ゲームループ本体
def main(player1:Player.Player, player2:Player.Player):
    start(player1, player2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        update(player1, player2)

#弾の衝突判定を行う
def getCollision(x1:float, x2:float, y1:float, y2:float, radius1:float, radius2:float):
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (radius1 + radius2) ** 2:
        return True
    else:
        return False

#弾の弱体化を行う
def setWeakening(bullet1P:Bullet.Bullet, bullet2P:Bullet.Bullet):
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
    
def collisionAlien(bullet:Bullet.Bullet, alien:Objects.Objects, player1:Player.Player, player2:Player.Player):
    alien.visible = False
    bullet.visible = False
    #1Pの弾と当たった時
    if bullet.bulletdirection == -1.0:
        player1.numberOfBlowAliens += 1
    #2Pの弾と当たった時
    else:
        player2.numberOfBlowAliens += 1

def collisionUFO(bullet:Bullet.Bullet, ufo:Objects.Objects, player1:Player.Player, player2:Player.Player):
    ufo.visible = False
    bullet.visible = False
    #1Pの弾と当たった時
    if bullet.bulletdirection == -1.0:
        player1.IsInvincible = True
    #2Pの弾と当たった時
    else:
        player2.IsInvincible = True

if __name__ == '__main__':
    main(Player.Player(True), Player.Player(False))