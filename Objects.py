#coding: "utf-8"
import pygame
import numpy as np

#タイプごとのID
UFO = 0 #UFO
ALIEN = 1 #エイリアン
#UFOの幅、高さ、半径
UFO_WIDTH = 100
UFO_HEIGHT = 50
UFO_RADIUS = 75
#エイリアンの幅、高さ、半径
ALIEN_WIDTH = 100
ALIEN_HEIGHT = 100
ALIEN_RADIUS = 50


class Objects:

    def __init__(self,x,y,type:int,moveToRightFlag:bool):
        self.x = x #x座標
        self.y = y #y座標
        self.type = type #タイプ(エイリアンかUFOか)
        self.moveToRightFlag = moveToRightFlag #右に行くか？(falseなら左に行く)
        if self.type == UFO:
           self.width = UFO_WIDTH #幅
           self.height = UFO_HEIGHT #高さ
           self.radius = UFO_RADIUS #半径
        elif self.type == ALIEN:
           self.width = ALIEN_WIDTH #幅
           self.height = ALIEN_HEIGHT #高さ
           self.radius = ALIEN_RADIUS #半径

