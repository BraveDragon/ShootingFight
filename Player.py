#coding: "utf-8"
import pygame
import Bullet
import numpy as np

Gunpoint_Speed = 20
MaxEnergy = 2000
StartEnergy = 1000
class Player:
    maxEnergy = MaxEnergy
    def __init__(self, is1P:bool, isAI:bool):
        #1P・2P共通部分の初期化
        #yはいらないかも
        self.is1P = is1P
        self.isAI = isAI
        self.currentEnergy = StartEnergy
        self.__x = 350
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
        
    
    #砲台の移動+弾を撃つ
    def Move(self, key=[], ai_input = -1 , bullets=[]):
        #プレイヤー操作時
        if self.isAI == False:
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
            #actionの値に応じて行動を決定
            action = np.argmax(ai_input)

            if action == 0:
                #左移動
                self.__x -= Gunpoint_Speed
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if action == 1:
                #右移動
                self.__x += Gunpoint_Speed
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if action == 2 and self.bulletweak_pressed_past != 1:
                #威力小の弾発射
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0

            if action == 3 and self.bulletmiddle_pressed_past != 1:
                #威力中の弾発射
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
            
            if action == 4 and self.bulletstrong_pressed_past != 1:
                #威力大の弾発射
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
            
            #移動+弾1つ撃ち
            if action == 5 and self.bulletweak_pressed_past != 1:
                #左移動+威力小の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0
            if action == 6 and self.bulletmiddle_pressed_past != 1:
                #左移動+威力中の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                
            if action == 7 and self.bulletstrong_pressed_past != 1:
                #左移動+威力大の弾発射
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
            
            if action == 8 and self.bulletweak_pressed_past != 1:
                #右移動+威力小の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.WEAK_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 0

            if action == 9 and self.bulletmiddle_pressed_past != 1:
                #右移動+威力中の弾発射
                self.__x += Gunpoint_Speed
                self.currentEnergy -= Bullet.MIDDLE_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
            
            if action == 10 and self.bulletstrong_pressed_past != 1:
                #右移動+威力大の弾発射
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= Bullet.STRONG_COST
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1

            #2種類の弾を発射
            if action == 11 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #小+中
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if action == 12 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #小+大
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if action == 13 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #中+大
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            #移動しながら2種類の弾を発射
            if action == 14 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #左移動+小+中
                self.__x -= Gunpoint_Speed
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if action == 15 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+小+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if action == 16 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+中+大
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            if action == 17 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1:
                #右移動+小+中
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 0
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
            
            if action == 18 and self.bulletweak_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #右移動+小+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 0
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))

            if action == 19 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #右移動+中+大
                self.__x += Gunpoint_Speed 
                self.currentEnergy -= (Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 0
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            #全発射
            if action == 20 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
                
            if action == 21 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
                #左移動+弾全発射
                self.__x -= Gunpoint_Speed 
                self.currentEnergy -= (Bullet.WEAK_COST + Bullet.MIDDLE_COST + Bullet.STRONG_COST)
                self.bulletweak_pressed_past = 1
                self.bulletmiddle_pressed_past = 1
                self.bulletstrong_pressed_past = 1
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_WEAK, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y, Bullet.BULLET_MIDDLE, self.bulletdirection))
                bullets.append(Bullet.Bullet(self.__x+25,self.y,Bullet.BULLET_STRONG, self.bulletdirection))
            
            if action == 22 and self.bulletweak_pressed_past != 1 and self.bulletmiddle_pressed_past != 1 and self.bulletstrong_pressed_past != 1:
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
        #TODO:画像サイズが違う場合に対応
        surface = pygame.display.get_surface()
        if self.__x <= 0:
            self.__x = 0
        if self.__x >= surface.get_width() - 100:
            self.__x = surface.get_width() - 100
    
    #ゲーム開始時の状態に戻す
    def Reset(self):
        self.maxEnergy = MaxEnergy
        self.currentEnergy = StartEnergy
        self.__x = 350

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
        
