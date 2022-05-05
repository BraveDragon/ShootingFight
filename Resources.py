import pygame
import Objects

#ゲームに使用する素材類を一括で管理するクラス
class Resources:
    player1 = pygame.image.load("Resources/GunPoint1P.png")
    player2 = pygame.image.load("Resources/GunPoint2P.png")
    ufo = pygame.image.load("Resources/UFO.png")
    #そのまま読みこむとUFOの画像は大きすぎるので、ここで縮小する
    ufo = pygame.transform.scale(ufo,[Objects.Objects.width,Objects.Objects.height])
