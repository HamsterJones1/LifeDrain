import pygame
from Globals import *
from Physics import PointRectCollision
from PositionVector import Position, Size
from Input import Input
from Text import Text


class Button:
    def __init__(self, position, size, effect=None, textString="", _format=None):
        self.pos = Position(*position)
        self.size = Size(*size)
        self.type = effect
        self.text = Text(textString, (self.pos.x + self.size.h / 4,
                                      self.pos.y + self.size.h / 4), int(2 * self.size.h / 3), black)
        if _format is not None:
            self.format = _format

        self.highlighted = False
        self.clicked = False

        self.color = white
        self.bColor = black
        self.hColor = black
        self.hbColor = white

    def setColor(self, color, bColor, hColor, hbColor):
        self.color = color
        self.bColor = bColor
        self.hColor = hColor
        self.hbColor = hbColor

    def updateText(self, text=None):
        if text is not None:
            self.text.updateText(text)

    def update(self, event, mouse):
        mousePos = Position(*mouse.get_pos())
        mousePos /= Globs.VIEW_SCALE
        self.highlighted = False
        self.clicked = False

        if PointRectCollision(self.pos, self.size, mousePos):
            self.highlighted = True
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == Input.interact):
                self.clicked = True

    def render(self, surface):
        if not self.highlighted:
            pygame.draw.rect(surface, self.color, [self.pos.x, self.pos.y, self.size.w, self.size.h], 0)
            pygame.draw.rect(surface, self.bColor, [self.pos.x, self.pos.y, self.size.w, self.size.h], 2)
            if self.text.canChangeColor:
                self.text.updateColor(self.hColor)
        else:
            pygame.draw.rect(surface, self.hColor, [self.pos.x, self.pos.y, self.size.w, self.size.h], 0)
            pygame.draw.rect(surface, self.hbColor, [self.pos.x, self.pos.y, self.size.w, self.size.h], 2)
            if self.text.canChangeColor:
                self.text.updateColor(self.color)

        self.text.render(surface, pygame.Rect(self.pos.x, self.pos.y, self.size.w, self.size.h), self.size.h / 4)
