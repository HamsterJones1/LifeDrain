import pygame
from Globals import *
from Audio import Audio
from Input import Input
from LevelManager import LevelManager
from MenuManager import MenuManager


class GameLoop:
    def __init__(self):
        # Window
        self.Window = pygame.display.set_mode(Globs.WINDOW_SIZE)
        pygame.display.set_caption("GameTest 0.0")
        self.display = pygame.Surface(Globs.VIEW_SIZE)

        # Audio
        self.audio = Audio()

        # Level
        self.curLevel = LevelManager(self.audio)
        self.menu = MenuManager()

    def Update(self):
        # Time
        Globs.dt = Globs.Clock.tick(Globs.FPS)

        # Input
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse

        # Quit
        if event.type == pygame.QUIT:
            Globs.RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                Globs.RUNNING = False
            if event.key == pygame.K_o:
                print(self.curLevel.player.pos.i)
            elif event.key == Input.pause and self.menu.current == "Paused":
                Globs.PAUSED ^= True

        # Window Resize
        if event.type == pygame.VIDEORESIZE:
            ResizeWindow(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        # Updates
        if not Globs.PAUSED and not Globs.DEAD:
            self.curLevel.update(event, keys, mouse)
            if Globs.DEAD:
                self.menu.loadMenu("Dead", self.curLevel)
        else:
            self.menu.update(event, mouse, self.curLevel)

        if Globs.WIN and self.audio.music != "Assets/Audio/Music/Monplaisir_-_04_-_Level_1.mp3":
            if not Globs.PAUSED:
                self.menu.loadMenu("Win", self.curLevel)

        if not Globs.MASTER_VOLUME or not Globs.MUSIC:
            self.audio.pause()
        elif not self.audio.playMusic and self.menu.current != "Dead":
            self.audio.play()

    def Render(self):
        # Background
        self.Window.fill(black)

        # Level
        self.curLevel.render(self.Window, self.display)

        if Globs.PAUSED:
            self.menu.render(self.display)

        if Globs.MASTER_VOLUME and Globs.MUSIC:
            self.audio.credit.render(self.display)

        # Render
        setDisplay = pygame.transform.scale(self.display, Globs.DISPLAY_SIZE)
        self.Window.blit(setDisplay, Globs.DISPLAY_OFFSET)
        pygame.display.flip()
