import pygame
import math
from random import randint
from Globals import *
from Physics import RectangleCollision, PointRectCollision, Hurtbox
from PositionVector import Position, Size
from Enemy import Enemy


# Set Enemy Type On Load -----------------------------------------------------------------------------------------------
class SetEnemy(Enemy):
    def __init__(self, position, variant="None"):
        super().__init__(position)
        if variant == "DefaultEnemy":
            self.__class__ = DefaultEnemy
        elif variant == "Archer":
            self.__class__ = Archer
        elif variant == "Heavy":
            self.__class__ = Heavy
        elif variant == "Wizard":
            self.__class__ = Wizard

        if self.__class__ != SetEnemy:
            self.__init__(position)


# Default --------------------------------------------------------------------------------------------------------------
class DefaultEnemy(Enemy):

    AnimationLengthDict = {'idle': 2,
                           'moving': 2,
                           'attacking': 2}
    FrameLengthDict = {'idle': 0.03,
                       'moving': 0.1,
                       'attacking': 0.05}
    ImageDict = {'idle': pygame.image.load(r"Assets/Images/Enemies/Default_Enemy_Idle.png"),
                 'moving': pygame.image.load(r"Assets/Images/Enemies/Default_Enemy_Walking.png"),
                 'attacking': pygame.image.load(r"Assets/Images/Enemies/Default_Enemy_Attacking.png")}

    def __init__(self, position):
        super().__init__(position)
        self.solid = False
        self.dealKnockback = Position(12, 8)
        self.variant = "DefaultEnemy"

    def render(self, surface, camOffset):
        # super().render(surface, camOffset)
        tmp = self.pos + camOffset
        tmp.x -= 24
        tmp.y -= 24
        # Directional
        if self.LR == 'R':
            # Animation
            surface.blit(DefaultEnemy.ImageDict[self.state], tmp.i, [int(self.curFrame) * 72, 0, 72, 72])
        else:
            image = DefaultEnemy.ImageDict[self.state]
            image = pygame.transform.flip(image, True, False)

            surface.blit(image, tmp.i, [(DefaultEnemy.AnimationLengthDict[self.state] -
                                         int(self.curFrame) - 1) * 72, 0, 72, 72])

    def animate(self):
        super().animate()

        # Check State
        if self.state != self.oldState:
            self.curFrame = 0
        self.oldState = self.state

        # Add Frames
        self.curFrame += DefaultEnemy.FrameLengthDict[self.state]

        # Loop
        if int(self.curFrame) >= DefaultEnemy.AnimationLengthDict[self.state]:
            self.curFrame = 0


# Archer ---------------------------------------------------------------------------------------------------------------
class Projectile:
    def __init__(self, originPosition, targetPosition):
        self.pos = Position(*originPosition)
        self.targetPos = Position(*targetPosition)
        self.hit = False
        self.dir = self.targetPos - self.pos
        length = math.hypot(*self.dir.i)
        if length == 0.0:
            self.dir.x = 0
            self.dir.y = -1
        else:
            self.dir.x = (self.dir.x / length)
            self.dir.y = (self.dir.y / length)

        self.angle = math.degrees(math.atan2(-self.dir.y, self.dir.x))
        self.spd = 2

    def update(self, curLevel):
        self.pos += self.dir * self.spd
        # Tilemap Collision
        for chunk in curLevel.tilemap.chunks:
            if chunk.loaded:
                for tile in chunk.tiles:
                    if tile.collision != "N":
                        if PointRectCollision(tile.pos, tile.size, self.pos):
                            self.hit = True

    def render(self, surface, camOffset):
        tmp = self.pos + camOffset
        pygame.draw.circle(surface, purple, tmp.i, 4, 0)
        pygame.draw.circle(surface, lightBlue, tmp.i, 3, 0)

        # image = pygame.transform.rotate(image, self.angle)


class Archer(Enemy):

    AnimationLengthDict = {'idle': 2,
                           'moving': 2,
                           'attacking': 4}
    FrameLengthDict = {'idle': 0.03,
                       'moving': 0.04,
                       'attacking': 0.05}
    ImageDict = {'idle': pygame.image.load(r"Assets/Images/Enemies/Wizard_Idle.png"),
                 'moving': pygame.image.load(r"Assets/Images/Enemies/Wizard_Walking.png"),
                 'attacking': pygame.image.load(r"Assets/Images/Enemies/Wizard_Attacking.png")}

    def __init__(self, position):
        super().__init__(position)
        self.variant = "Archer"
        self.size = Size(32, 64)

        # Movement
        self.acc = 0.05
        self.maxSpd = 1

        # Game States
        self.solid = False

        # Gameplay
        self.health = 69
        self.hurtbox = Hurtbox(self.center.i, (0, 0))
        self.hurtbox.solid = False
        self.damage = 35
        self.projectileList = []

        # Timers
        self.setAttackCooldown = 10

    def update(self, curLevel):
        super().update(curLevel)
        self.updateProjectiles(curLevel)

    def updateProjectiles(self, curLevel):
        if len(self.projectileList) > 15:
            self.projectileList = []
            self.state = "idle"
        if self.state == "attacking" and self.attackCooldown <= 0:
            self.projectileList.append(Projectile(self.center.i, curLevel.player.center.i))

        removeList = []
        for proj in self.projectileList:
            proj.update(curLevel)
            if proj.hit:
                removeList.append(proj)
        for proj in removeList:
            self.projectileList.remove(proj)

    def render(self, surface, camOffset):
        # super().render(surface, camOffset)
        for proj in self.projectileList:
            proj.render(surface, camOffset)

        tmp = self.pos + camOffset
        tmp.y -= 8
        # Directional
        if self.LR == 'R':
            # Animation

            surface.blit(Archer.ImageDict[self.state], tmp.i, [int(self.curFrame) * 32, 0, 32, 72])
        else:
            image = Archer.ImageDict[self.state]
            image = pygame.transform.flip(image, True, False)
            surface.blit(image, tmp.i, [(Archer.AnimationLengthDict[self.state] -
                                         int(self.curFrame) - 1) * 32, 0, 32, 72])

    def animate(self):
        super().animate()

        # Check State
        if self.state != self.oldState:
            self.curFrame = 0
        self.oldState = self.state

        # Add Frames
        self.curFrame += Archer.FrameLengthDict[self.state]

        # Loop
        if int(self.curFrame) >= Archer.AnimationLengthDict[self.state]:
            self.curFrame = 0


class Wizard(Archer):
    def __init__(self, pos):
        super().__init__(pos)
        self.variant = "Wizard"

    def update(self, curLevel):
        super().update(curLevel)
        if self.state == "moving":
            self.state = "attacking"


# Heavy ----------------------------------------------------------------------------------------------------------------
class Heavy(Enemy):

    AnimationLengthDict = {'idle': 2,
                           'moving': 2,
                           'attacking': 2}
    FrameLengthDict = {'idle': 0.03,
                       'moving': 0.04,
                       'attacking': 0.05}
    ImageDict = {'idle': pygame.image.load(r"Assets/Images/Enemies/Heavy_Idle.png"),
                 'moving': pygame.image.load(r"Assets/Images/Enemies/Heavy_Walking.png"),
                 'attacking': pygame.image.load(r"Assets/Images/Enemies/Heavy_Attacking.png")}

    def __init__(self, position):
        super().__init__(position)
        self.variant = "Heavy"
        self.size = Size(64, 80)

        # Movement
        self.acc = 0.05
        self.maxSpd = 1.5

        # Game States
        self.solid = True

        # Gameplay
        self.health = 420
        self.hurtbox = Hurtbox(self.center.i, (90, 40))
        self.hurtbox.solid = True
        self.damage = 55
        self.projectileList = []

        # Timers
        self.setAttackCooldown = 6.5

    def update(self, curLevel):
        super().update(curLevel)
        if self.stun > 0:
            self.stun -= 6

    @property
    def center(self):
        tmp = self.pos + self.size / 2
        tmp.y -= 10
        return tmp

    def render(self, surface, camOffset):
        # super().render(surface, camOffset)
        for proj in self.projectileList:
            proj.render(surface, camOffset)

        tmp = self.pos + camOffset
        tmp.y -= 20
        tmp.x -= 30
        # Directional
        offsetX = 120
        if self.state == "attacking":
            offsetX = 180
            tmp.x -= 20
        if self.LR == 'R':

            # Animation
            surface.blit(Heavy.ImageDict[self.state], tmp.i, [int(self.curFrame) * offsetX, 0, offsetX, 100])
        else:
            image = Heavy.ImageDict[self.state]
            image = pygame.transform.flip(image, True, False)
            surface.blit(image, tmp.i, [(Heavy.AnimationLengthDict[self.state] -
                                         int(self.curFrame) - 1) * offsetX, 0, offsetX, 100])

    def animate(self):
        # super().animate()
        # Check State
        if self.state != self.oldState:
            self.curFrame = 0
        self.oldState = self.state

        # Add Frames
        self.curFrame += Heavy.FrameLengthDict[self.state]

        # Loop
        if int(self.curFrame) >= Heavy.AnimationLengthDict[self.state]:
            self.curFrame = 0

    def handleKnockback(self, deltaPos):
        pass
