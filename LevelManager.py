import pygame
from Globals import *
from Tilemap import Tilemap
from Camera import Camera
from Player import Player
from Enemy import Enemy
from EnemyVariants import DefaultEnemy, Archer, Heavy, Wizard
from Door import Door


class LevelManager:
    def __init__(self, audio):
        self.num = 0

        # Level Utility
        self.tilemap = None
        self.door = None
        self.camera = Camera()

        # Entities
        self.player = Player()
        self.enemiesList = []
        # self.itemsList = []

        # Load Level
        self.loadLevel(self.num)

        # Audio
        self.audio = audio

    def loadLevel(self, number):
        self.num = number

        if self.num == 0:
            self.tilemap = Tilemap(r"Assets\TextFiles\Tilemaps\Tilemap_A.txt")
            self.door = Door((3680, 352), (32, 64))
            self.player.resetAllValues((350, 480), self.camera)
            self.enemiesList = [DefaultEnemy((700, 455)), DefaultEnemy((2145, 360)), DefaultEnemy((1884, 390)),
                                DefaultEnemy((1100, 490)), DefaultEnemy((2340, 230)), DefaultEnemy((2740, 490)),
                                DefaultEnemy((2830, 490)), Archer((3030, 444)), DefaultEnemy((3525, 365)),
                                Archer((3595, 365)), Archer((3715, 365))]
        elif self.num == 1:
            self.tilemap = Tilemap(r"Assets\TextFiles\Tilemaps\Tilemap_B.txt")
            self.door = Door((5294, 898), (32, 64))
            self.player.setPosition((350, 480), self.camera)
            self.enemiesList = [DefaultEnemy((980, 1035)), DefaultEnemy((1625, 1130)), Archer((1731, 1120)),
                                Archer((2214, 1060)), Wizard((1825, 925)), DefaultEnemy((2300, 970)),
                                DefaultEnemy((2200, 970)), Heavy((3000, 1040)), Wizard((3050, 1040)),
                                DefaultEnemy((3650, 1030)), DefaultEnemy((3700, 1030)), Wizard((4190, 960)),
                                Wizard((5184, 900)), Heavy((5100, 890)), DefaultEnemy((5011, 976)),
                                Heavy((4712, 866)), Archer((4642, 866))]

        else:
            Globs.WIN = True

    def update(self, event, key, mouse):
        self.door.update(self.player)
        if self.door.entered:
            self.loadLevel(self.num + 1)

        # Entities
        self.player.update(event, key, mouse, self)
        removalList = []
        for enemy in self.enemiesList:
            enemy.update(self)
            if enemy.dead:
                removalList.append(enemy)
        for enemy in removalList:
            self.enemiesList.remove(enemy)

        # Load Chunks
        for chunk in self.tilemap.chunks:
            tmp = chunk.pos - self.player.pos
            if -Globs.RENDER_DISTANCE[0] <= tmp.x <= Globs.RENDER_DISTANCE[0] and\
                    -Globs.RENDER_DISTANCE[1] <= tmp.y <= Globs.RENDER_DISTANCE[1]:
                chunk.loaded = True
            else:
                chunk.loaded = False

    def render(self, window, surface):
        # Render Level
        self.camera.render(window, surface, self)
