#coding: "utf-8"
import Game
from Player import Player

if __name__ == '__main__':
    Player1 = Player(True)
    Player2 = Player(False)
    Game.main(Player1, Player2)