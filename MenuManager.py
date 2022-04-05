import pygame
from Globals import *
from SaveLoad import SaveGame, LoadGame
from PositionVector import Position
from Tilemap import Tilemap
from Button import Button
from Text import Text
from Input import Input
from DetectInput import DetectInput
from Player import Player
from EnemyVariants import DefaultEnemy


class MenuManager:
    def __init__(self):
        self.current = "Main"
        self.buttonsList = []
        self.textList = []
        self.tilemap = Tilemap(r"Assets\TextFiles\Tilemaps\Menu.txt")

        self.i = 0

        self.loadMenu(self.current)

    def loadMenu(self, menuType=None, curLevel=None):
        if menuType is not None:
            self.current = menuType

        if self.current == "Paused":
            self.textList = []
            self.buttonsList = [Button((55, 55), (120, 30),  "Play", "play"),
                                Button((55, 100), (120, 30), "Menu", "menu"),
                                Button((55, 145), (120, 30), "Save", "save")]
        elif self.current == "Main":
            self.textList = [Text("life drain", (19, 19), 30, red), Text("life drain", (20, 20), 30, white),
                             Text("life drain", (21, 21), 30, black)]
            self.buttonsList = [Button((25, 240), (155, 30),  "Resume", "resume"),
                                Button((215, 200), (155, 30), "Settings", "settings"),
                                Button((25, 200), (155, 30),  "NewGame", "new game"),
                                Button((215, 240), (155, 30), "Quit", "quit")]
        elif self.current == "Settings":
            self.textList = [Text("life drain", (19, 19), 30, red), Text("life drain", (20, 20), 30, white),
                             Text("life drain", (21, 21), 30, black)]
            self.buttonsList = [Button((25, 200), (155, 30),  "Menu", "back"),
                                Button((215, 240), (155, 30), "Input", "controls"),
                                Button((25, 240), (155, 30),  "Load", "load game"),
                                Button((215, 200), (155, 30), "Audio", "audio")]
        elif self.current == "Audio":
            self.textList = []
            mv = mu = se = "false"
            if Globs.MASTER_VOLUME:
                mv = "true"
            if Globs.MUSIC:
                mu = "true"
            if Globs.SOUND_EFFECTS:
                se = "false"
            self.buttonsList = [Button((25, 160), (155, 30),  "Settings", "back"),
                                Button((25, 30), (350, 30), "Bool", "volume = " + mv, "Volume"),
                                Button((25, 70), (350, 30), "Bool", "music = " + mu, "Music"),
                                Button((25, 110), (350, 30), "Bool", "sound effects = " + se, "Effects")]
        elif self.current == "ChangeInput":
            self.textList = [Text(" click to change", (15, 250), 10, white)]
            self.buttonsList = [Button((260, 260), (130, 25), "Settings", "back"),
                                Button((15, 15), (130, 25), "Change", "left = " + chr(Input.left), Input.left),
                                Button((15, 50), (130, 25), "Change", "right = " + chr(Input.right), Input.right),
                                Button((15, 85), (130, 25), "Change", "jump = " + chr(Input.jump), Input.jump),
                                Button((15, 120), (130, 25), "Change", "duck = " + chr(Input.duck), Input.duck),
                                Button((15, 155), (130, 25), "Change", "attk = " + chr(Input.attack), Input.attack),
                                Button((165, 85), (220, 25), "X", "dash = shift"),
                                Button((165, 15), (220, 25), "X", "f11 = fullscreen"),
                                Button((15, 190), (130, 25), "Change", "pick = " + chr(Input.interact), Input.interact),
                                Button((165, 50), (220, 25), "X", "pause = esc"),
                                Button((165, 120), (220, 25), "X", "attk = l-click")]
        # ...
        elif self.current == "Dead":
            curLevel.audio.pause()
            self.textList = [Text("you died", (49, 49), 20, white), Text("you died", (50, 50), 20, red)]
            self.buttonsList = [Button((25, 200), (155, 30),  "Menu", "main menu")]
        elif self.current == "Win":
            curLevel.audio.credit.updateColor(white)
            Globs.PAUSED = True
            curLevel.audio.loadMusic("Assets/Audio/Music/Monplaisir_-_04_-_Level_1.mp3")
            self.textList = [Text("you win", (24, 24), 40, white), Text("you win", (25, 25), 40, red),
                             Text("had to cut short. sorry.", (5, 260), 20, white)]
            self.buttonsList = [Button((25, 200), (155, 30),  "Menu", "main menu")]

    def update(self, event, mouse, curLevel):
        for button in self.buttonsList:
            button.update(event, mouse)
            if button.clicked:
                self.buttonClicked(button, curLevel)

    def render(self, surface):
        surface.fill(black)

        # Behind the Buttons
        if self.current == "Main":
            surface.fill(lightBlue)
            self.tilemap.render(surface, Position(0, 10))
            self.i += 0.03
            if self.i >= 2:
                self.i = 0
            surface.blit(Player.ImageDict["idle"], (32, 122), [int(self.i) * 48, 0, 48, 48])
        elif self.current == "Settings":
            surface.fill(lightBlue)
            self.tilemap.render(surface, Position(0, 10))
            self.i += 0.03
            if self.i >= 2:
                self.i = 0
            surface.blit((pygame.transform.flip(DefaultEnemy.ImageDict["idle"], True, False)), (100, 100),
                         [int(self.i) * 72, 0, 72, 72])
            surface.blit((pygame.transform.flip(DefaultEnemy.ImageDict["idle"], True, False)), (300, 68),
                         [int(self.i) * 72, 0, 72, 72])
        elif self.current == "Paused":
            pygame.draw.rect(surface, black, [50, 50, 300, 200], 0)
        elif self.current == "Dead":
            pass

        # Text
        for text in self.textList:
            text.render(surface)

        # The Buttons
        for button in self.buttonsList:
            button.render(surface)

    # Button Functionality
    def buttonClicked(self, button, curLevel):
        # Play
        if button.type == "Play":
            Globs.PAUSED = False
        # Menu
        elif button.type == "Menu":
            curLevel.audio.credit.updateColor(black)
            Globs.PAUSED = True
            if curLevel.audio.music != "Assets/Audio/Music/Komiku_-_12_-_Bicycle.mp3":
                curLevel.audio.pause()
            if not curLevel.audio.playMusic:
                curLevel.audio.loadMusic("Assets/Audio/Music/Komiku_-_12_-_Bicycle.mp3")
            self.loadMenu("Main")
        # Resume
        elif button.type == "Resume":
            if Globs.WIN:
                self.loadMenu("Win", curLevel)
            if not Globs.DEAD:
                Globs.PAUSED = False
                self.loadMenu("Paused")
                curLevel.audio.loadMusic("Assets/Audio/Music/Komiku_-_02_-_We_need_a_plan.mp3")
            else:
                self.loadMenu("Dead", curLevel)
                curLevel.audio.pause()
        # NewGame
        elif button.type == "NewGame":
            Globs.WIN = False
            Globs.DEAD = False
            Globs.PAUSED = False
            self.loadMenu("Paused")
            curLevel.audio.loadMusic("Assets/Audio/Music/Komiku_-_02_-_We_need_a_plan.mp3")
            curLevel.loadLevel(0)
        # Settings
        elif button.type == "Settings":
            Globs.PAUSED = True
            self.loadMenu("Settings")
        # Input
        elif button.type == "Input":
            Globs.PAUSED = True
            self.loadMenu("ChangeInput")
        # Audio
        elif button.type == "Audio":
            self.loadMenu("Audio")
        # Bool
        elif button.type == "Bool":
            if button.format == "Volume":
                Globs.MASTER_VOLUME ^= True
            elif button.format == "Music":
                Globs.MUSIC ^= True
            elif button.format == "Effects":
                Globs.SOUND_EFFECTS ^= True
            self.loadMenu("Audio")
        # Change
        elif button.type == "Change":
            try:
                value = ord(DetectInput("enter new key:", 1, (50, 125), (300, 50), True, False, True, False))
                if button.format == Input.left:
                    Input.left = value
                elif button.format == Input.right:
                    Input.right = value
                elif button.format == Input.jump:
                    Input.jump = value
                elif button.format == Input.duck:
                    Input.duck = value
                elif button.format == Input.attack:
                    Input.attack = value
                elif button.format == Input.interact:
                    Input.interact = value
            except:
                pass

            self.loadMenu("ChangeInput")
        # Save
        elif button.type == "Save":
            tempStr = "Assets/TextFiles/Saves/"
            tempStr += DetectInput("save name")
            tempStr += ".txt"
            SaveGame(curLevel, tempStr)
        # Load
        elif button.type == "Load":
            Globs.WIN = False
            tempStr = "Assets/TextFiles/Saves/"
            tempStr += DetectInput("save name")
            tempStr += ".txt"
            try:
                LoadGame(curLevel, tempStr)
                curLevel.audio.loadMusic("Assets/Audio/Music/Komiku_-_02_-_We_need_a_plan.mp3")
                Globs.DEAD = False
                self.loadMenu("Paused")
                Globs.PAUSED = False
            except:
                pass
        # Quit
        elif button.type == "Quit":
            Globs.RUNNING = False

