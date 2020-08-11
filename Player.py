import pygame

class Player:
    def __init__(self, is1P:bool, isAI:bool, maxEnergy:int, startEnergy:int):
        #1P・2P共通部分の初期化
        #yはいらないかも
        self.is1P = is1P
        self.isAI = isAI
        self.maxEnergy = maxEnergy
        self.currentEnergy = startEnergy
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
    
    #移動させる(左に動かす時はマイナスの数値を指定)
    def Move(self,direction:float):
            self.__x += direction
            #行き過ぎの抑制
            #TODO:画像サイズが違う場合に対応
            surface = pygame.display.get_surface()
            if self.__x <= 0:
                self.__x = 0
            if self.__x >= surface.get_width() - 100:
                self.__x = surface.get_width() - 100
    
    def GetX(self):
        return self.__x
        
        #TODO: AI対応(Agentクラスやそのラッパークラスで対応した方が良いかも)
