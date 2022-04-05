import pygame
from Globals import *
from Physics import RectangleCollision
from PositionVector import Position, Size


class Door:

    Image = pygame.image.load("Assets/Images/Door.png")

    def __init__(self, position, size):
        self.pos = Position(*position)
        self.size = Size(*size)
        self.entered = False

    def update(self, player):
        if RectangleCollision(self.pos, self.size, player.pos, player.size):
            self.entered = True

    def render(self, surface, camOffset):
        tmp = self.pos + camOffset
        # pygame.draw.rect(surface, black, [tmp.x, tmp.y, self.size.w, self.size.h], 0)
        surface.blit(Door.Image, tmp.i)
