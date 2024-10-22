import pygame
import Objects

#ゲームに使用する素材類を一括で管理するクラス
class Resources:
    def __init__(self):
        self.player1 = pygame.image.load("Resources/GunPoint1P.png").convert_alpha()
        self.player2 = pygame.image.load("Resources/GunPoint2P.png").convert_alpha()
        ufo = pygame.image.load("Resources/UFO.png").convert_alpha()
        #そのまま読みこむとUFOの画像は大きすぎるので、ここで縮小する
        self.ufo = pygame.transform.scale(ufo,[Objects.UFO_WIDTH,Objects.UFO_HEIGHT]).convert_alpha()
        #そのまま読みこむとエイリアンの画像は大きすぎるので、ここで縮小する
        alien = pygame.image.load("Resources/Alien.png").convert_alpha()
        self.alien = pygame.transform.scale(alien,[Objects.ALIEN_WIDTH,Objects.ALIEN_HEIGHT]).convert_alpha()
