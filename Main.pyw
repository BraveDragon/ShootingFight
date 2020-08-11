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



#初期化処理
def start():
    global screen
    pygame.init()
    #TODO: タイトルをマシにする
    pygame.display.set_caption("ShootingFight")
    screen = pygame.display.set_mode((Width, Height))
    clock = pygame.time.Clock()
    clock.tick(60)
    font = pygame.font.Font(None, 80)
    global resource
    resource = Resources.Resources()
    global Player1
    global Player2
    global Bullets
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

    #画面を黒く塗りつぶす
    screen.fill((0,0,0,0))

    if Player1.currentEnergy < Player1.maxEnergy:
        Player1.currentEnergy += 1
    
    if Player2.currentEnergy < Player2.maxEnergy:
        Player2.currentEnergy += 1

    #キーボード入力を受け取る
    key = pygame.key.get_pressed()
    #1P
    #移動
    if key[Player1.left] == 1:
        Player1.Move(-Gunpoint_Speed)
    if key[Player1.right] == 1:
        Player1.Move(Gunpoint_Speed)
    #弾を撃つ
    #TODO: 弾を撃ったらエネルギーを減らす
    #押し離しで弾を撃つ
    #異種の弾の同時撃ちは禁止した方が良いかもしれない
    #威力小の弾
    bulletweak_pressed_now1P = key[Player1.bulletweak]
    if bulletweak_pressed_now1P == 1 and Player1.bulletweak_pressed_past != 1:
        Bullets.append(Bullet.Bullet(Player1.GetX()+25,Player1.y, Bullet.BULLET_WEAK, Player1.bulletdirection))
    Player1.bulletweak_pressed_past = bulletweak_pressed_now1P
    #威力中の弾
    bulletmiddle_pressed_now1P = key[Player1.bulletmiddle]
    if bulletmiddle_pressed_now1P == 1 and Player1.bulletmiddle_pressed_past != 1:
        Bullets.append(Bullet.Bullet(Player1.GetX()+25,Player1.y, Bullet.BULLET_MIDDLE, Player1.bulletdirection))
    Player1.bulletmiddle_pressed_past = bulletmiddle_pressed_now1P
    #威力大の弾
    bulletstrong_pressed_now1P = key[Player1.bulletstrong]
    if bulletstrong_pressed_now1P == 1 and Player1.bulletstrong_pressed_past != 1:
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
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_WEAK, Player2.bulletdirection))
    Player2.bulletweak_pressed_past = bulletweak_pressed_now2P
    #威力中の弾
    bulletmiddle_pressed_now2P = key[Player2.bulletmiddle]
    if bulletmiddle_pressed_now2P == 1 and Player2.bulletmiddle_pressed_past != 1:
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_MIDDLE, Player2.bulletdirection))
    Player2.bulletmiddle_pressed_past = bulletmiddle_pressed_now2P
    #威力大の弾
    bulletstrong_pressed_now2P = key[Player2.bulletstrong]
    if bulletstrong_pressed_now2P == 1 and Player2.bulletstrong_pressed_past != 1:
        Bullets.append(Bullet.Bullet(Player2.GetX()+25,Player2.y, Bullet.BULLET_STRONG, Player2.bulletdirection))
    Player2.bulletstrong_pressed_past = bulletstrong_pressed_now2P
    

    #弾の描画
    for bullet in Bullets:
        bullet.draw(screen)
    #画面外に出た弾を消す(実際は画面内にある弾だけ抽出している)
    Bullets = [bullet for bullet in Bullets if bullet.visible == True]
    
    #砲台(プレイヤー操作)の描画
    screen.blit(resource.player1,[Player1.GetX(),Player1.y])
    screen.blit(resource.player2,[Player2.GetX(),Player2.y])

    #エネルギーバーの描画
    #1P
    pygame.draw.rect(screen, (255,255,255), [10, 570, Player1.currentEnergy*0.25, 20])
    #2P
    pygame.draw.rect(screen, (255,255,255), [290, 10, Player2.currentEnergy*0.25, 20])
    #TODO: 残りエネルギーで色を変える
    
    

#メインループ
def main():
    start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        update()


if __name__ == '__main__':
    main()