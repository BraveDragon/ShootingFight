#coding: "utf-8"
#ゲーム本体用
import pygame
import sys
import Objects
from Resources import Resources
import Bullet
import Player
import numpy as np

MAX_UFOs = 1
MAX_Aliens = 2
Bullets : list[Bullet.Bullet] = []
UFOs : list[Objects.Objects] = []
Aliens: list[Objects.Objects] = []
Width = 800
Height = 600

pygame.init()
pygame.display.set_caption("ShootingFight")
screen = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
resource : Resources = Resources()
clock : pygame.time.Clock = None

#初期化処理
def start(player1:Player.Player, player2:Player.Player):
    global Bullets
    global UFOs
    global Aliens
    
    Bullets = []
    UFOs = []
    Aliens = []
    player1.Reset()
    player2.Reset()

#ゲームの処理
def update(player1:Player.Player,
           player2:Player.Player,
           P1Input:int=-1,
           P2Input:int=-1) -> tuple[tuple[np.ndarray, int, int], bool, int, int]:
    #グローバル宣言
    global screen
    global resource
    global Bullets
    global UFOs
    global Aliens
    #最大フレームレートを30fpsで固定
    clock = pygame.time.Clock()
    clock.tick(30)

    #キーボード入力を受け取る
    key = pygame.key.get_pressed()
    #勝敗判定
    if player1.currentEnergy <= 0 or player2.currentEnergy <= 0:
        Result(player1,player2, key, screen)
        #ここでupdate()を打ち切る
        return getObservation(player1, player2)
    
    #画面を黒く塗りつぶす
    screen.fill((0,0,0,0))
    
    if player1.currentEnergy < Player.Player.maxEnergy:
        player1.currentEnergy += 10
    
    if player2.currentEnergy < Player.Player.maxEnergy:
        player2.currentEnergy += 10
    

    #弾の描画
    for bullet in Bullets:
        bullet.draw(screen,player1,player2)

    #画面外に出た弾を消す(実際は画面内にある弾だけ抽出している)
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]

    #弾の衝突判定+弱体化
    player1Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == player1.bulletDirection]
    player2Bullets = [bullet for bullet in Bullets if bullet.bulletDirection == player2.bulletDirection]

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
                collisionUFO(bullet,ufo,player1,player2)
    
    #UFOに当たった弾を削除
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]
    #弾に当たったエイリアンを削除
    UFOs = [ufo for ufo in UFOs if ufo.visible == True]

    #各プレイヤーの動き
    player1.Move(key=key, bullets=Bullets, ai_input=P1Input)
    player2.Move(key=key, bullets=Bullets, ai_input=P2Input)
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1, [player1.GetX(),player1.y])
    screen.blit(resource.player2, [player2.GetX(),player2.y])
    #エイリアンの生成
    if len(Aliens) <= MAX_Aliens:
        x = np.random.rand() * (Width / 2)
        y = np.random.rand() * (Height * 0.5) + 100
        LorR = np.random.rand()
        if LorR > 0.5:
            Aliens.append(Objects.Objects(x, y, Objects.ALIEN, moveToRightFlag=True))
        else:
            Aliens.append(Objects.Objects(x, y, Objects.ALIEN, moveToRightFlag=False))
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
            UFOs.append(Objects.Objects(x, y, Objects.UFO, moveToRightFlag=True))
        else:
            UFOs.append(Objects.Objects(x, y, Objects.UFO, moveToRightFlag=False))
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

    return getObservation(player1, player2)

def Result(player1:Player.Player,player2:Player.Player, key:tuple, surface: pygame.Surface) -> tuple[int, int]:
    #結果の文字表示
    font = pygame.font.Font(None, 200)
    if key[pygame.K_SPACE]:
        start(player1, player2)
    #引き分け時
    if player1.currentEnergy <= 0 and player2.currentEnergy <= 0: 
        text = font.render("DRAW", True, (255, 255, 255))
        surface.blit(text,[150, 250])
    #1P敗北時
    elif player1.currentEnergy <= 0:
        text = font.render("2P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
    #2P敗北時
    else:
        text = font.render("1P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])

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
def getCollision(x1:float, x2:float, y1:float, y2:float, radius1:float, radius2:float) -> bool:
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (radius1 + radius2) ** 2:
        return True
    else:
        return False

#弾の弱体化を行う
def setWeakening(bullet1P:Bullet.Bullet, bullet2P:Bullet.Bullet):
    b1afterLevel = bullet1P.bulletLevel - bullet2P.bulletLevel
    b2afterLevel = bullet2P.bulletLevel - bullet1P.bulletLevel
    bullet1P.bulletLevel = b1afterLevel
    bullet2P.bulletLevel = b2afterLevel
    #1Pの弾
    #弾の弱体化+消滅
    if bullet1P.bulletLevel <= 0:
        bullet1P.visible = False
    elif bullet1P.bulletLevel == 1:
        bullet1P.bulletType = Bullet.BULLET_WEAK
    else:
        bullet1P.bulletType = Bullet.BULLET_MIDDLE
    
    #2Pの弾
    #弾の弱体化+消滅
    if bullet2P.bulletLevel <= 0:
        bullet2P.visible = False
    elif bullet2P.bulletLevel == 1:
        bullet2P.bulletType = Bullet.BULLET_WEAK
    else:
        bullet2P.bulletType = Bullet.BULLET_MIDDLE
    
def collisionAlien(bullet:Bullet.Bullet, alien:Objects.Objects, player1:Player.Player, player2:Player.Player):
    alien.visible = False
    bullet.visible = False
    #1Pの弾と当たった時
    if bullet.bulletDirection == -1.0:
        player1.numberOfBlowAliens += 1
    #2Pの弾と当たった時
    else:
        player2.numberOfBlowAliens += 1

def collisionUFO(bullet:Bullet.Bullet, ufo:Objects.Objects, player1:Player.Player, player2:Player.Player):
    ufo.visible = False
    bullet.visible = False
    #1Pの弾と当たった時
    if bullet.bulletDirection == -1.0:
        player1.IsInvincible = True
    #2Pの弾と当たった時
    else:
        player2.IsInvincible = True

def getReward(p1energy : int, p2energy: int) -> tuple[int, int]:
    if p1energy <= 0 and p2energy <= 0:
        return (-1, -1)
    elif p1energy <= 0:
        return (-1, 1)
    elif p2energy <= 0:
        return (1, -1)
    else:
        return (0, 0)

def getObservation(player1:Player.Player, player2: Player.Player) -> tuple[np.ndarray, bool, int, int]:
    gameWindow = pygame.surfarray.array3d(pygame.display.get_surface())
    P1reward, P2reward = getReward(player1.currentEnergy, player2.currentEnergy)
    finishedFlag = False if P1reward == 0 and P2reward == 0 else True
    return (gameWindow, finishedFlag, P1reward, P2reward)
