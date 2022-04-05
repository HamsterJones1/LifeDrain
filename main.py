import pygame
from Globals import Globs
from GameLoop import GameLoop

pygame.init()

Globs.MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
Game = GameLoop()

while Globs.RUNNING:
    Game.Update()
    Game.Render()

pygame.quit()
