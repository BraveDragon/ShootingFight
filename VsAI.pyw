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

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Player1 = Player.Player(True)
Player2 = Player.Player(False)

Model2P = Agent.Agent().to(DEVICE)
Model2P.load_state_dict(torch.load("Model2P.pth"))
Model2P.eval()

#ゲームループ本体
def main():
    Game.start(Player1, Player2)
    input_frames = 4
    window_dim = 3
    InputDeque = deque(maxlen=input_frames)
    InputDeque.extend(np.zeros((input_frames, window_dim, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        #最大フレームレートを30fpsで固定
        clock = pygame.time.Clock()
        clock.tick(30)
        with torch.no_grad():
            Input = np.array(InputDeque).reshape((1, -1, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale)))
            Input = torch.from_numpy(Input).float().to(DEVICE)
            action2P = torch.argmax(Model2P(Input)).cpu().detach().numpy()
        NextObservation, finishedFlag, _, _ = Game.update(Player1, Player2, P2Input=action2P)
        InputDeque.append(Agent.convertStateToAgent(NextObservation, Agent.scale))
        if finishedFlag == True:
            InputDeque.extend(np.zeros((input_frames, window_dim, int(Game.Width * Agent.scale), int(Game.Height * Agent.scale))))

if __name__ == '__main__':
    main()