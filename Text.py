import pygame
from PositionVector import Position
from Globals import *


class Text:
    Fonts = {}

    def __init__(self, text, position, fontSize=16, color=black, highlight=None):
        # Class Variables

        self.font = Text.Fonts[fontSize] = pygame.font.Font(r"Assets\Fonts\Font_JdP.ttf", fontSize)
        self.text = str(text)
        self.pos = Position(*position)
        self.size = fontSize

        self.color = color
        self.canChangeColor = True
        self.background = highlight

    def updateText(self, text=None):
        if text is not None:
            self.text = str(text)

    def updateColor(self, color, background=None):
        self.color = color
        self.background = background

    def render(self, surface, rect=None, offset=None):
        tmp = self.font.render(self.text, False, self.color, self.background)

        if rect is None:
            surface.blit(tmp, self.pos.i)
        else:
            surface.blit(tmp, rect, pygame.Rect(-offset, -offset, rect.w, rect.h))

