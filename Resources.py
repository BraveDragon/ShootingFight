import pygame

#ゲームに使用する素材類を一括で管理するクラス
class Resources:
    def __init__(self):
        self.player1 = pygame.image.load("Resources/GunPoint1P.png")
        self.player2 = pygame.image.load("Resources/GunPoint2P.png")
        self.ufo = pygame.image.load("Resources/UFO.png")
        
    pass

