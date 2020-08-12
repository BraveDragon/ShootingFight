import pygame
import sys
import Resources
import Player
import Bullet


Bullets = []
resource = None
screen = None
clock = None
Player1 = None
Player2 = None

Width = 800
Height = 600
Gunpoint_Speed = 1
Player1 = Player.Player(True,False,2000, 1000)
Player2 = Player.Player(False,False,2000, 1000)


#初期化処理
def start():
    global screen
    pygame.init()
    #TODO: タイトルをマシにする
    pygame.display.set_caption("ShootingFight")
    screen = pygame.display.set_mode((Width, Height))
    clock = pygame.time.Clock()
    clock.tick(60)
    global resource
    resource = Resources.Resources()
    global Player1
    global Player2
    global Bullets
    Bullets = []
    Player1 = Player.Player(True,False,2000, 1000)
    Player2 = Player.Player(False,False,2000, 1000)
    


#ゲームの処理
def update():
    #グローバル宣言
    global screen
    global resource
    global Player1
    global Player2
    global Bullets

    #キーボード入力を受け取る
    key = pygame.key.get_pressed()
    #勝敗判定
    if Player1.currentEnergy <= 0 or Player2.currentEnergy <= 0:
        Result(Player1, Player2, key, screen)
        #ここでupdate()を打ち切る
        return
    
    #画面を黒く塗りつぶす
    screen.fill((0,0,0,0))
    
    if Player1.currentEnergy < Player1.maxEnergy:
        Player1.currentEnergy += 0.2
    
    if Player2.currentEnergy < Player2.maxEnergy:
        Player2.currentEnergy += 0.2
    
    #1P
    #移動
    if key[Player1.left] == 1:
        Player1.Move(-Gunpoint_Speed)
    if key[Player1.right] == 1:
        Player1.Move(Gunpoint_Speed)
    #弾を撃つ
    #弾を撃ったらエネルギーを減らす
    #押し離しで弾を撃つ
    #異種の弾の同時撃ちは禁止した方が良いかもしれない
    #威力小の弾
    bulletweak_pressed_now1P = key[Player1.bulletweak]
    if bulletweak_pressed_now1P == 1 and Player1.bulletweak_pressed_past != 1:
        Player1.currentEnergy -= Bullet.WEAK_DAMAGE
        Bullets.append(Bullet.Bullet(Player1.GetX()+25,Player1.y, Bullet.BULLET_WEAK, Player1.bulletdirection))
    Player1.bulletweak_pressed_past = bulletweak_pressed_now1P
    #威力中の弾
    bulletmiddle_pressed_now1P = key[Player1.bulletmiddle]
    if bulletmiddle_pressed_now1P == 1 and Player1.bulletmiddle_pressed_past != 1:
        Player1.currentEnergy -= Bullet.MIDDLE_DAMAGE
        Bullets.append(Bullet.Bullet(Player1.GetX()+25,Player1.y, Bullet.BULLET_MIDDLE, Player1.bulletdirection))
    Player1.bulletmiddle_pressed_past = bulletmiddle_pressed_now1P
    #威力大の弾
    bulletstrong_pressed_now1P = key[Player1.bulletstrong]
    if bulletstrong_pressed_now1P == 1 and Player1.bulletstrong_pressed_past != 1:
        Player1.currentEnergy -= Bullet.STRONG_DAMAGE
        Bullets.append(Bullet.Bullet(Player1.GetX()+25,Player1.y, Bullet.BULLET_STRONG, Player1.bulletdirection))
    Player1.bulletstrong_pressed_past = bulletstrong_pressed_now1P

    #2P
    #移動
    if key[Player2.left] == 1:
        Player2.Move(-Gunpoint_Speed)
    if key[Player2.right] == 1:
        Player2.Move(Gunpoint_Speed)
    
    #弾を撃つ
    #押し離しで弾を撃つ
    #異種の弾の同時撃ちは禁止した方が良いかもしれない
    #威力小の弾
    bulletweak_pressed_now2P = key[Player2.bulletweak]
    if bulletweak_pressed_now2P == 1 and Player2.bulletweak_pressed_past != 1:
        Player2.currentEnergy -= Bullet.WEAK_DAMAGE
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_WEAK, Player2.bulletdirection))
    Player2.bulletweak_pressed_past = bulletweak_pressed_now2P
    #威力中の弾
    bulletmiddle_pressed_now2P = key[Player2.bulletmiddle]
    if bulletmiddle_pressed_now2P == 1 and Player2.bulletmiddle_pressed_past != 1:
        Player2.currentEnergy -= Bullet.MIDDLE_DAMAGE
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_MIDDLE, Player2.bulletdirection))
    Player2.bulletmiddle_pressed_past = bulletmiddle_pressed_now2P
    #威力大の弾
    bulletstrong_pressed_now2P = key[Player2.bulletstrong]
    if bulletstrong_pressed_now2P == 1 and Player2.bulletstrong_pressed_past != 1:
        Player2.currentEnergy -= Bullet.STRONG_DAMAGE
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_STRONG, Player2.bulletdirection))
    Player2.bulletstrong_pressed_past = bulletstrong_pressed_now2P
    

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
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1,[Player1.GetX(),Player1.y])
    screen.blit(resource.player2,[Player2.GetX(),Player2.y])

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
    #結果の文字表示
    font = pygame.font.Font(None, 200)
    #1P敗北時
    if player1.currentEnergy <= 0:
        text = font.render("2P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])
    #2P敗北時
    else:
        text = font.render("1P WIN!", True, (255, 255, 255))
        surface.blit(text,[150, 250])

    if key[pygame.K_SPACE]:
        start()

    


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