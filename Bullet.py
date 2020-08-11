import pygame
import sys
import Player
import Main
BULLET_SPEED = 0.5
#色を定義。弾に使用する
BULLET_STRONG = (255, 0, 0) #威力強の弾
BULLET_MIDDLE = (0, 255, 0) #威力中の弾
BULLET_WEAK = (0, 0, 255) #威力小の弾

class Bullet:
    #弾の大きさ
    BULLET_RADIUS = 25

    def __init__(self, x, y, bullettype, bulletdirection):
        self.x = x
        self.y = y
        self.bullettype = bullettype
        self.bulletdirection = bulletdirection
        #画面から見えるか？
        self.visible = True
    
    def draw(self, surface):
        if self.BULLET_RADIUS <= self.y <= Main.Height:
            pygame.draw.circle(surface,self.bullettype,[int(self.x + self.BULLET_RADIUS), int(self.y)], self.BULLET_RADIUS)
        else:
            self.visible = False
            #TODO: 相手陣に弾が届いたらその分相手のエネルギーを減らす
            
        self.y += BULLET_SPEED * self.bulletdirection
        #TODO: 弾同士の衝突判定
        
        
        
        