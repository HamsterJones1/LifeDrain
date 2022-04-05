import pygame
from Globals import *


class Input:
    # Player Movement
    left = pygame.K_a
    right = pygame.K_d
    jump = pygame.K_w
    duck = pygame.K_s

    sprint = pygame.K_LSHIFT
    # longDash = pygame.K_SPACE
    # shortDash = pygame.K_LCTRL

    attack = pygame.K_r

    # Menu Navigation
    pause = pygame.K_ESCAPE

    interact = pygame.K_e
    # inventory = pygame.K_TAB
    # trueInventory = pygame.K_i


def saveKeyboardLayout(file="Save_1"):
    fileLocation = "Assets/TextFiles/KeyboardLayout/" + file
    pass


def loadKeyboardLayout(self, file="Save_1"):
    fileLocation = "Assets/TextFiles/KeyboardLayout/" + file
    readFile = open(fileLocation, "r")
    lines = readFile.readlines()
    readFile.close()

    for line in lines:
        key, value = line.split("=")
        if key == "Left":
            Input.left = value

        # ...
