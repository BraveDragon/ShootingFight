#coding: "utf-8"
import pygame
import numpy as np

class UFO:
    width = 100 #幅
    height = 50 #高さ

    def __init__(self,x,y,type:int,moveToRightFlag:bool):
        self.x = x #x座標
        self.y = y #y座標
        self.type = type #タイプ
        self.moveToRightFlag = moveToRightFlag #右に行くか？(falseなら左に行く)