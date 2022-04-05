import pygame
import pygame.gfxdraw
from random import randint
from PositionVector import Position, Size
from Globals import *


class Camera:
    def __init__(self):
        self.offset = Position(0, 0)
        self.trueOffset = self.offset
        self.size = Size(*Globs.VIEW_SIZE)
        self.size = Size(*Globs.WINDOW_SIZE)

    def setOffset(self, deltaPosition, clear=False):
        if clear:
            pass
        # self.trueOffset -= deltaPosition
        # self.offset -= 2 * deltaPosition / 3
        self.offset -= deltaPosition

    def updateOffset(self):
        pass

    def render(self, window, surface, curLevel):
        # Update Offset
        # self.updateOffset()

        # Set Clipping Rectangle
        window.set_clip([int(self.offset.x), int(self.offset.y), int(self.size.w), int(self.size.h)])

        # Fill Background
        surface.fill(blue)

        # Current Level
        curLevel.tilemap.render(surface, self.offset)

        curLevel.door.render(surface, self.offset)

        for enemy in curLevel.enemiesList:
            enemy.render(surface, self.offset)

        curLevel.player.render(surface, self.offset)

        # Reset Clipping Rectangle
        window.set_clip(None)

