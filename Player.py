#coding: "utf-8"
import pygame
import Bullet

Gunpoint_Speed = 20
MaxEnergy = 2000
StartEnergy = 1000
InvincibleTime = 300 #無敵時間(1秒60フレームなので、300フレーム=5秒となる)
class Player:
    maxEnergy = MaxEnergy
    def __init__(self, is1P:bool):
        #1P・2P共通部分の初期化
        #yはいらないかも
        self.is1P = is1P
        self.currentEnergy = StartEnergy
        self.__x = 350
        self.bulletWeak_pressed_past = 0
        self.bulletMiddle_pressed_past = 0
        self.bulletStrong_pressed_past = 0
        self.numberOfBlowAliens = 0 #エイリアンの撃破数(この数だけ攻撃力が上がる)
        self.IsInvincible = False #無敵状態か？(UFOを倒すと、5秒だけ無敵になれる)
        self.InvincibleCount = 0 #無敵状態のカウント(毎フレーム1加算。InvincibleTimeを超えれば無敵状態を解除)

        if self.is1P == True:
            self.left = pygame.K_a
            self.right = pygame.K_s
            self.bulletWeak = pygame.K_e
            self.bulletMiddle = pygame.K_r
            self.bulletStrong = pygame.K_t
            self.bulletDirection = -1.0
            self.y = 500
    
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.bulletWeak = pygame.K_COMMA
            self.bulletMiddle = pygame.K_PERIOD
            self.bulletStrong = pygame.K_SLASH
            self.bulletDirection = 1.0
            self.y = 50
        
    
    #砲台の移動+弾を撃つ
    def Move(self, key=[], ai_input : int = -1, bullets=[]):
        
        #プレイヤー操作時
        if ai_input == -1:
            #移動
            if key[self.left] == 1:
                self.__x -= Gunpoint_Speed
            if key[self.right] == 1:
                self.__x += Gunpoint_Speed
            
            #弾を撃つ
            #弾を撃ったらエネルギーを減らす
            #押し離しで弾を撃つ
            #異種の弾の同時撃ちは禁止した方が良いかもしれない

            #威力小の弾
            bulletWeak_pressed_now = key[self.bulletWeak]
            if bulletWeak_pressed_now == 1 and self.bulletWeak_pressed_past != 1:
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
            self.bulletWeak_pressed_past = bulletWeak_pressed_now
            #威力中の弾
            bulletMiddle_pressed_now = key[self.bulletMiddle]
            if bulletMiddle_pressed_now == 1 and self.bulletMiddle_pressed_past != 1:
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
            self.bulletMiddle_pressed_past = bulletMiddle_pressed_now
            #威力大の弾
            bulletStrong_pressed_now = key[self.bulletStrong]
            if bulletStrong_pressed_now == 1 and self.bulletStrong_pressed_past != 1:
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_STRONG, self.bulletDirection))
            self.bulletStrong_pressed_past = bulletStrong_pressed_now
        #AI操作時
        else:

            if ai_input == 0:
                #左移動
                self.__x -= Gunpoint_Speed
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 0
            if ai_input == 1:
                #右移動
                self.__x += Gunpoint_Speed
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 0
            if ai_input == 2 and self.bulletWeak_pressed_past != 1:
                #威力小の弾発射
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 0

            if ai_input == 3 and self.bulletMiddle_pressed_past != 1:
                #威力中の弾発射
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
            
            if ai_input == 4 and self.bulletStrong_pressed_past != 1:
                #威力大の弾発射
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1
            
            #移動+弾1つ撃ち
            if ai_input == 5 and self.bulletWeak_pressed_past != 1:
                #左移動+威力小の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 0
            if ai_input == 6 and self.bulletMiddle_pressed_past != 1:
                #左移動+威力中の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
                
            if ai_input == 7 and self.bulletStrong_pressed_past != 1:
                #左移動+威力大の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1
            
            if ai_input == 8 and self.bulletWeak_pressed_past != 1:
                #右移動+威力小の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 0

            if ai_input == 9 and self.bulletMiddle_pressed_past != 1:
                #右移動+威力中の弾発射
                self.__x += Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
            
            if ai_input == 10 and self.bulletStrong_pressed_past != 1:
                #右移動+威力大の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1

            #2種類の弾を発射
            if ai_input == 11 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1:
                #小+中
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
            
            if ai_input == 12 and self.bulletWeak_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #小+大
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))

            if ai_input == 13 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #中+大
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
            
            #移動しながら2種類の弾を発射
            if ai_input == 14 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1:
                #左移動+小+中
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
            
            if ai_input == 15 and self.bulletWeak_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #左移動+小+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))

            if ai_input == 16 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #左移動+中+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
            
            if ai_input == 17 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1:
                #右移動+小+中
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
            
            if ai_input == 18 and self.bulletWeak_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #右移動+小+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 0
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))

            if ai_input == 19 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #右移動+中+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 0
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
            
            #全発射
            if ai_input == 20 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
                
            if ai_input == 21 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #左移動+弾全発射
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
            
            if ai_input == 22 and self.bulletWeak_pressed_past != 1 and self.bulletMiddle_pressed_past != 1 and self.bulletStrong_pressed_past != 1:
                #右移動+弾全発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletWeak_pressed_past = 1
                self.bulletMiddle_pressed_past = 1
                self.bulletStrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletDirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletDirection))
            
        
        #行き過ぎの抑制
        surface = pygame.display.get_surface()
        if self.__x <= 0:
            self.__x = 0
        if self.__x >= surface.get_width() - 100:
            self.__x = surface.get_width() - 100
        
        if self.IsInvincible == True:
            self.InvincibleCount += 1
        
        if self.InvincibleCount >= InvincibleTime:
            self.IsInvincible = False
            self.InvincibleCount = 0
    
    #ゲーム開始時の状態に戻す
    def Reset(self):
        self.maxEnergy = MaxEnergy
        self.currentEnergy = StartEnergy
        self.__x = 350
        self.IsInvincible = False
        self.InvincibleCount = 0

        self.bulletWeak_pressed_past = 0
        self.bulletMiddle_pressed_past = 0
        self.bulletStrong_pressed_past = 0

        if self.is1P == True:
            self.left = pygame.K_a
            self.right = pygame.K_s
            self.bulletWeak = pygame.K_e
            self.bulletMiddle = pygame.K_r
            self.bulletStrong = pygame.K_t
            self.bulletDirection = -1.0
            self.y = 500
            
            
        
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.bulletWeak = pygame.K_COMMA
            self.bulletMiddle = pygame.K_PERIOD
            self.bulletStrong = pygame.K_SLASH
            self.bulletDirection = 1.0
            self.y = 50

    def GetX(self):
        return self.__x
        
