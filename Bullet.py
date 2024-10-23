#coding: "utf-8"
import pygame

BULLET_SPEED = 20
#色を定義。弾に使用する
BULLET_STRONG = (255, 0, 0) #威力強の弾
BULLET_MIDDLE = (0, 255, 0) #威力中の弾
BULLET_WEAK = (0, 0, 255) #威力小の弾
WEAK_DAMAGE = 200
MIDDLE_DAMAGE = 400
STRONG_DAMAGE = 600
WEAK_COST = 100
MIDDLE_COST = 200
STRONG_COST = 300
#弾の大きさ
BULLET_RADIUS = 25
AttackBonus = 10 #エイリアンを1体倒すごとに得られる攻撃力ボーナス(ダメージがこの数値分増える)

class Bullet:
    
    def __init__(self, x : float, y : float, bulletType : tuple[int, int,int], bulletDirection : float):
        self.x = x
        self.y = y
        self.bulletType = bulletType
        self.bulletDirection = bulletDirection
        #画面から見えるか？
        self.visible = True
        #弾の強さ
        #弱：1, 中：2, 強：3
        if self.bulletType == BULLET_WEAK:
            self.bulletLevel : int = 1
        elif self.bulletType == BULLET_MIDDLE:
            self.bulletLevel : int = 2
        else:
            self.bulletLevel : int = 3

    def draw(self, surface, player1, player2):
        height = pygame.display.get_surface().get_height()
        if BULLET_RADIUS <= self.y <= height and self.visible == True:
            pygame.draw.circle(surface,self.bulletType,[int(self.x + BULLET_RADIUS), int(self.y)], BULLET_RADIUS)
        else:
            self.visible = False
            #相手陣に弾が届いたらその分相手のエネルギーを減らす
            #エイリアンを倒した分のボーナスダメージも同時に入る
            #1Pの弾
            if self.bulletDirection == -1.0 and player2.IsInvincible == False:
                if self.bulletType == BULLET_WEAK:
                    player2.currentEnergy -= (WEAK_DAMAGE + AttackBonus * player1.numberOfBlowAliens)
                elif self.bulletType == BULLET_MIDDLE:
                    player2.currentEnergy -= (MIDDLE_DAMAGE + AttackBonus * player1.numberOfBlowAliens)
                else:
                    player2.currentEnergy -= (STRONG_DAMAGE + AttackBonus * player1.numberOfBlowAliens)
            #2Pの弾        
            elif player1.IsInvincible == False:
                if self.bulletType == BULLET_WEAK:
                    player1.currentEnergy -= (WEAK_DAMAGE + AttackBonus * player2.numberOfBlowAliens)
                elif self.bulletType == BULLET_MIDDLE:
                    player1.currentEnergy -= (MIDDLE_DAMAGE + AttackBonus * player2.numberOfBlowAliens)
                else:
                    player1.currentEnergy -= (STRONG_DAMAGE + AttackBonus * player2.numberOfBlowAliens)

            
        self.y += BULLET_SPEED * self.bulletDirection
        
        
        
        