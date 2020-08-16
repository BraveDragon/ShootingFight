#coding: "utf-8"
import pygame
import Bullet

Gunpoint_Speed = 1
MaxEnergy = 2000
StartEnergy = 1000
class Player:
    def __init__(self, is1P:bool, isAI:bool):
        #1P・2P共通部分の初期化
        #yはいらないかも
        self.is1P = is1P
        self.isAI = isAI
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
        
    
    #砲台の移動+弾を撃つ
    def Move(self, key=(), ai_input=[], bullets=[]):
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
            
            pass    

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
        
        #TODO: AI対応(Agentクラスやそのラッパークラスで対応した方が良いかも)
