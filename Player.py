#coding: "utf-8"
import pygame
import Bullet
import numpy as np

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
        self.bulletweak_pressed_past = 0
        self.bulletmiddle_pressed_past = 0
        self.bulletstrong_pressed_past = 0
        self.numberOfBlowAliens = 0 #エイリアンの撃破数(この数だけ攻撃力が上がる)
        self.IsInvincible = False #無敵状態か？(UFOを倒すと、5秒だけ無敵になれる)
        self.InvincibleCount = 0 #無敵状態のカウント(毎フレーム1加算。InvincibleTimeを超えれば無敵状態を解除)

        if self.is1P == True:
            self.left = pygame.K_a
            self.right = pygame.K_s
            self.bulletweak = pygame.K_e
            self.bulletmiddle = pygame.K_r
            self.bulletstrong = pygame.K_t
            self.bulletdirection = -1.0
            self.y = 500
    
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.bulletweak = pygame.K_COMMA
            self.bulletmiddle = pygame.K_PERIOD
            self.bulletstrong = pygame.K_SLASH
            self.bulletdirection = 1.0
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
            bulletweak_pressed_now = key[self.bulletweak]
            if bulletweak_pressed_now == 1 and self.bulletweak_pressed_past != 1:
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
            self.bulletweak_pressed_past = bulletweak_pressed_now
            #威力中の弾
            bulletmiddle_pressed_now = key[self.bulletmiddle]
            if bulletmiddle_pressed_now == 1 and self.bulletmiddle_pressed_past != 1:
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            self.bulletmiddle_pressed_past = bulletmiddle_pressed_now
            #威力大の弾
            bulletstrong_pressed_now = key[self.bulletstrong]
            if bulletstrong_pressed_now == 1 and self.bulletstrong_pressed_past != 1:
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_STRONG, self.bulletdirection))
            self.bulletstrong_pressed_past = bulletstrong_pressed_now
        #AI操作時
        else:

            if ai_input == 0:
                #左移動
                self.__x -= Gunpoint_Speed
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if ai_input == 1:
                #右移動
                self.__x += Gunpoint_Speed
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if ai_input == 2 and self.bulletweak_pressed_past != 1:
                #威力小の弾発射
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0

            if ai_input == 3 and self.bulletmiddle_pressed_past != 1:
                #威力中の弾発射
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
            
            if ai_input == 4 and self.bulletstrong_pressed_past != 1:
                #威力大の弾発射
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
            
            #移動+弾1つ撃ち
            if ai_input == 5 and self.bulletweak_pressed_past != 1:
                #左移動+威力小の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if ai_input == 6 and self.bulletmiddle_pressed_past != 1:
                #左移動+威力中の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                
            if ai_input == 7 and self.bulletstrong_pressed_past != 1:
                #左移動+威力大の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
            
            if ai_input == 8 and self.bulletweak_pressed_past != 1:
                #右移動+威力小の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0

            if ai_input == 9 and self.bulletmiddle_pressed_past != 1:
                #右移動+威力中の弾発射
                self.__x += Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
            
            if ai_input == 10 and self.bulletstrong_pressed_past != 1:
                #右移動+威力大の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1

            #2種類の弾を発射
            if ai_input == 11 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #小+中
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if ai_input == 12 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #小+大
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if ai_input == 13 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #中+大
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            #移動しながら2種類の弾を発射
            if ai_input == 14 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #左移動+小+中
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if ai_input == 15 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+小+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if ai_input == 16 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+中+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            if ai_input == 17 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #右移動+小+中
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if ai_input == 18 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #右移動+小+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if ai_input == 19 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #右移動+中+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            #全発射
            if ai_input == 20 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                
            if ai_input == 21 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+弾全発射
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            if ai_input == 22 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #右移動+弾全発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
        
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

        self.bulletweak_pressed_past = 0
        self.bulletmiddle_pressed_past = 0
        self.bulletstrong_pressed_past = 0

        if self.is1P == True:
            self.left = pygame.K_a
            self.right = pygame.K_s
            self.bulletweak = pygame.K_e
            self.bulletmiddle = pygame.K_r
            self.bulletstrong = pygame.K_t
            self.bulletdirection = -1.0
            self.y = 500
            
            
        
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.bulletweak = pygame.K_COMMA
            self.bulletmiddle = pygame.K_PERIOD
            self.bulletstrong = pygame.K_SLASH
            self.bulletdirection = 1.0
            self.y = 50

    def GetX(self):
        return self.__x
        
