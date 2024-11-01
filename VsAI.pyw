#coding: "utf-8"
#プレイヤー VS AI
#ゲーム本体用
import pygame
import sys
import Game
import Player
#AI用
import Agent
import torch
import numpy as np
from collections import deque

screen : pygame.Surface = None
clock = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

memsize = 10000
batch_size = 32
JustLooking = 10
current_episode = 0

Player1 = Player.Player(True)
Player2 = Player.Player(False)

Model2P = Agent.Agent().to(DEVICE)
Model2P.load_state_dict(torch.load("Model2P.pth"))
Model2P.eval()

#ゲームループ本体
def main():
    Game.start(Player1, Player2)
    input_frames = 4
    InputDeque = deque(maxlen=input_frames)
    for _ in range(input_frames):
        InputDeque.append(np.zeros((int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        #最大フレームレートを30fpsで固定
        clock = pygame.time.Clock()
        clock.tick(30)
        state, _, _, _ = Game.getObservation(Player1, Player2)
        InputDeque.append(Agent.convertStateToAgent(state, Agent.scale))
        with torch.no_grad():
            Input = torch.from_numpy(np.array(InputDeque)).float().to(DEVICE)
            action2P =  torch.argmax(Model2P(Input)).cpu().detach().numpy()
        Game.update(Player1, Player2, P2Input=action2P)

if __name__ == '__main__':
    main()