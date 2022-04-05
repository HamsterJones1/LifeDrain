import pygame
from random import randint
from Globals import *
from Physics import RectangleCollision, Hurtbox
from PositionVector import Position, Size


class Enemy:
    def __init__(self, position):
        self.pos = Position(*position)
        self.dead = False
        self.size = Size(32, 48)

        # Movement
        self.acc = 0.25
        self.spd = 0
        self.maxSpd = 5
        self.yAcc = Globs.GRAVITY_ACC
        self.ySpd = 0
        self.yMaxSpd = Globs.GRAVITY_MAX
        self.jumpSpd = 14
        self.onGround = False
        self.dealKnockback = Position(0, 0)
        self.takeKnockback = Position(0, 0)

        # Game States
        self.state = "idle"
        self.LR = 'L'
        self.UD = 'U'
        self.solid = True

        # Gameplay
        self.health = 100
        self.hurtbox = Hurtbox(self.center.i, (48, 32))
        self.hurtbox.collision = "LR"
        self.damage = 19
        self.projectileList = None

        # Timers
        self.healthDrain = 0
        self.attackCooldown = 0
        self.setAttackCooldown = 3
        self.stun = 0
        self.iFrames = 0
        self.actionTimer = 0

        # Animation
        self.curFrame = 0
        self.oldState = self.state

    @property
    def center(self):
        return self.pos + self.size / 2

    def makeChoice(self, forceChoice=None):
        """Chose between idle, moving, attacking or defending.
        Random at the moment but has potential for educated choices.
        If you are reading this, hi! :)"""

        if self.actionTimer <= 0:
            self.actionTimer = randint(120, 300)

            # Make Choice
            if forceChoice is None:
                choiceNumber = randint(1, 3)
            else:
                choiceNumber = forceChoice

            # Act upon it
            if choiceNumber == 1:
                # Move
                self.state = "moving"
            elif choiceNumber == 2:
                # Attack
                self.state = "attacking"
            elif choiceNumber == 3:
                # Idle
                self.state = "idle"
        else:
            self.actionTimer -= 1

    # UPDATE -----------------------------------------------------------------------------------------------------------
    def update(self, curLevel):
        # Update if within Render Distance
        player = curLevel.player
        if abs(player.pos.x - self.pos.x) < Globs.RENDER_DISTANCE[0] / 2 and\
                abs(player.pos.y - self.pos.y) < Globs.RENDER_DISTANCE[1] / 2:

            # Set Defaults
            self.hurtbox.active = False
            self.UD = "U"
            self.onGround = False

            # Direction
            if player.center.x < self.center.x:
                self.LR = "L"
            else:
                self.LR = "R"
            # UD

            # Make a Decision
            self.makeChoice()

            # Attack
            if self.state == "attacking":
                if self.attackCooldown <= 0:
                    self.generateHurtbox()
                    self.attackCooldown = self.setAttackCooldown
                else:
                    self.updateAttackCooldown()

            # Gravity
            if not self.onGround:
                self.ySpd += self.yAcc

            # Update Status
            self.updateHealth()
            if self.iFrames > 0:
                self.iFrames -= 1

            # Speed Cap
            self.speedCap()

            # Update Movement
            if self.stun <= 0:
                self.move()
            else:
                self.stun -= 1
                self.spd = 0

            # Friction
            if self.state != "moving":
                if self.spd > 0.25:
                    self.spd -= self.acc
                elif self.spd < -0.25:
                    self.spd += self.acc
                else:
                    self.spd = 0

            # Test New Position
            deltaPos = Position(int(self.spd), int(self.ySpd))

            # Player Collision
            if player.hurtbox.active:
                if self.collision(deltaPos, [player.hurtbox], True, False):
                    self.healthDrain += player.damage
                    self.iFrames = 10
                    self.stun = 40
                    self.handleKnockback(deltaPos)

            # Tilemap Collision
            for chunk in curLevel.tilemap.chunks:
                if chunk.loaded:
                    self.collision(deltaPos, chunk.collisionTiles)

            # Set New Position
            self.pos += deltaPos

            self.animate()

    # RENDER -----------------------------------------------------------------------------------------------------------
    def render(self, surface, camOffset):
        tmp = self.pos + camOffset
        if self.iFrames <= 0:
            pygame.draw.rect(surface, magenta, [tmp.x, tmp.y, self.size.w, self.size.h])
        else:
            pygame.draw.rect(surface, white, [tmp.x, tmp.y, self.size.w, self.size.h])
        if self.hurtbox.active:
            tmpbox = self.hurtbox.pos + camOffset
            pygame.draw.rect(surface, red, [tmpbox.x, tmpbox.y, self.hurtbox.size.w, self.hurtbox.size.h])

    # METHODS ----------------------------------------------------------------------------------------------------------
    def collision(self, deltaPos, tileSet, solid=True, knockback=False):
        returnValue = False
        for other in tileSet:
            # Vertical Collision
            if other.collision != "L" and other.collision != "R" and other.collision != "LR":
                tmp = deltaPos.copy()
                tmp.x = 0
                if RectangleCollision(self.pos + tmp, self.size, other.pos, other.size):
                    returnValue = True

                    # Top Side
                    if self.pos.y < other.pos.y and other.collision != "B" and not self.onGround:
                        if solid:
                            self.ySpd = 0
                            self.onGround = True
                            deltaPos.y = (other.pos.y - self.pos.y - self.size.h)
                        if knockback:
                            self.takeKnockback.y -= other.dealKnockback.y
                    # Bottom Side
                    else:
                        if solid:
                            self.ySpd = 0
                            deltaPos.y = (other.pos.y + other.size.h - self.pos.y)
                        if knockback:
                            self.takeKnockback.y += other.dealKnockback.y

            # Horizontal Collision
            if other.collision != "T" and other.collision != "B":
                tmp = deltaPos.copy()
                tmp.y = 0
                if RectangleCollision(self.pos + tmp, self.size, other.pos, other.size):
                    returnValue = True

                    # Left Side
                    if self.pos.x < other.pos.x and other.collision != "R":
                        if solid:
                            self.spd = 0
                            deltaPos.x = (other.pos.x - self.pos.x - self.size.w)
                        if knockback:
                            self.takeKnockback.x -= other.dealKnockback.x
                    # Right Side
                    else:
                        if solid:
                            self.spd = 0
                            deltaPos.x = (other.pos.x + other.size.w - self.pos.x)
                        if knockback:
                            self.takeKnockback.x += other.dealKnockback.x
        return returnValue

    def handleKnockback(self, deltaPos):
        pass
        """
        deltaPos.x += self.takeKnockback.x
        deltaPos.y += self.takeKnockback.y
        self.takeKnockback.x = 0
        self.takeKnockback.y = 0"""

    def move(self):
        # Move
        if self.state == "moving":
            if self.LR == "L":
                self.spd -= self.acc
            else:
                self.spd += self.acc

    def speedCap(self):
        if self.spd >= self.maxSpd:
            self.spd = self.maxSpd
        elif self.spd <= -self.maxSpd:
            self.spd = -self.maxSpd
        if self.ySpd >= self.yMaxSpd:
            self.ySpd = self.yMaxSpd
        elif self.ySpd <= -self.yMaxSpd:
            self.ySpd = -self.yMaxSpd

    def updateAttackCooldown(self):
        if self.attackCooldown > 0:
            self.attackCooldown -= 0.15
        elif self.attackCooldown < 0:
            self.attackCooldown = 0

    def updateHealth(self):
        if self.health <= 0:
            self.dead = True
        if self.healthDrain > 0:
            self.health -= 1.5
            self.healthDrain -= 1.5

    def generateHurtbox(self):
        self.hurtbox.active = True
        if self.LR == "L":
            self.hurtbox.pos.x = self.center.x - self.hurtbox.size.w
        else:
            self.hurtbox.pos.x = self.center.x
        self.hurtbox.pos.y = self.center.y - self.hurtbox.size.h / 2

    def animate(self):
        pass
