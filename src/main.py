import pygame
import sys
import os
current_path = os.path.abspath(__file__)
top_path = "\\".join(current_path.split('\\')[:-2])
sys.path.append(top_path)

from pygame.locals import *
from const import *
from game import *

pygame.init()

DS = pygame.display.set_mode( GAME_SIZE )
game = Game(DS)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouseClickHandler(event.button)
    game.update()
    DS.fill( (255, 255, 255 ) )
    game.draw()
    pygame.display.update()

