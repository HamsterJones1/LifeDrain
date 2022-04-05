import pygame
from Globals import *
from Physics import RectangleCollision, PointRectCollision, Hurtbox
from PositionVector import Position, Size
from Input import Input as Key


class Player:

    AnimationLengthDict = {'idle': 2,
                           'moving': 4,
                           'sprinting': 2,
                           'attacking': 1,
                           'jumping': 1,
                           'ducking': 2,
                           'duck_attacking': 1}
    FrameLengthDict = {'idle': 0.03,
                       'moving': 0.1,
                       'sprinting': 0.2,
                       'attacking': 0,
                       'jumping': 0,
                       'ducking': 0,
                       'duck_attacking': 0}
    ImageDict = {'idle': pygame.image.load(r"Assets/Images/Player/Old_Man_Idle.png"),
                 'moving': pygame.image.load(r"Assets/Images/Player/Old_Man_Walking.png"),
                 'sprinting': pygame.image.load(r"Assets/Images/Player/Old_Man_Sprinting.png"),
                 'attacking': pygame.image.load(r"Assets/Images/Player/Old_Man_Attacking.png"),
                 'jumping': pygame.image.load(r"Assets/Images/Player/Old_Man_Jumping.png"),
                 'ducking': pygame.image.load(r"Assets/Images/Player/Old_Man_Ducking.png"),
                 'duck_attacking': pygame.image.load(r"Assets/Images/Player/Old_Man_Duck_Attacking.png")}
    UIDict = {"HFalse": pygame.image.load("Assets/Images/UI/H50.png"),
              "HTrue": pygame.image.load("Assets/Images/UI/H100.png"),
              "SFalse": pygame.image.load("Assets/Images/UI/S50.png"),
              "STrue": pygame.image.load("Assets/Images/UI/S100.png")}

    def __init__(self):
        self.pos = Position(184, 200)
        self.size = Size(32, 48)
        self.defaultSize = self.size
        self.duckSize = Size(32, 24)

        # Movement
        self.acc = 0.25
        self.spd = 0
        self.maxSpd = 4
        self.yAcc = Globs.GRAVITY_ACC
        self.ySpd = 0
        self.yMaxSpd = Globs.GRAVITY_MAX
        self.jumpSpd = 10
        self.onGround = False
        self.offGroundTimer = 0
        self.dealKnockback = Position(12, -8)
        self.takeKnockback = Position(0, 0)

        # Game States
        self.hasControl = True
        self.state = "idle"
        self.LR = 'L'
        self.UD = 'U'
        self.pD = False

        # Gameplay
        self.health = 100
        self.setHealth = self.health
        self.maxSetHealth = self.health + 2
        self.stamina = 75
        self.setStamina = self.stamina
        self.maxSetStamina = self.stamina + 2

        self.damage = 35
        self.hurtbox = Hurtbox(self.center.i, (48, 64))

        # Timers
        self.staminaDrain = 0
        self.healthDrain = 0
        self.attackCooldown = 1
        self.iFrames = 0

        # Animation
        self.curFrame = 0
        self.oldState = self.state

    @property
    def center(self):
        return self.pos + self.size / 2

    def setPosition(self, position, camera, load=False):
        deltaPos = Position(*position) - self.pos
        self.pos += deltaPos
        if load:
            deltaPos.y -= 25

        camera.setOffset(deltaPos)

    def setSize(self, size):
        self.size = Size(*size)

    def resetAllValues(self, position, camera):
        self.setPosition(position, camera)
        self.size = self.defaultSize
        # Movement
        self.spd = 0
        self.maxSpd = 4
        self.ySpd = 0
        self.onGround = False
        self.offGroundTimer = 0
        # Game States
        self.hasControl = True
        self.state = "idle"
        self.LR = 'L'
        self.UD = 'U'
        self.pD = False
        # Gameplay
        self.health = 100
        self.setHealth = self.health
        self.stamina = 75
        self.setStamina = self.stamina
        # Timers
        self.staminaDrain = 0
        self.healthDrain = 0
        self.attackCooldown = 1

    # UPDATE -----------------------------------------------------------------------------------------------------------
    def update(self, event, keys, mouse, curLevel):
        if self.hasControl:
            # Set Priority Defaults
            self.hurtbox.active = False
            self.UD = "U"
            self.state = "idle"

            # Input
            if keys[Key.duck]:
                self.UD = "D"
            if event.type == pygame.KEYDOWN and event.key == Key.duck and not self.pD:
                self.pos.y += self.size.h - self.duckSize.h
                self.size = self.duckSize
                self.pD = True
            elif (event.type == pygame.KEYUP and event.key == Key.duck and self.pD) or (self.pD and self.UD == "U"):
                self.size = self.defaultSize
                self.pos.y -= self.size.h - self.duckSize.h
                self.pD = False

            if keys[Key.sprint]:
                self.state = "sprinting"
                if self.stamina > 0:
                    self.maxSpd = 8
                    if self.spd != 0:
                        self.stamina -= 0.5
            if keys[Key.left]:
                self.spd -= self.acc
                self.LR = 'L'
                if self.state != "sprinting":
                    self.state = "moving"
            if keys[Key.right]:
                self.spd += self.acc
                self.LR = 'R'
                if self.state != "sprinting":
                    self.state = "moving"
            if keys[Key.jump] and self.onGround and self.stamina >= 15:
                self.ySpd -= self.jumpSpd
                self.onGround = False
                self.staminaDrain += 15
            if (keys[Key.attack] or mouse.get_pressed()[0]) and self.stamina >= 7 and self.attackCooldown == 0:
                self.state = "attacking"
                self.generateHurtbox()
                self.staminaDrain += 7
                self.attackCooldown = 5

            # Gravity
            if not self.onGround:
                self.ySpd += self.yAcc
                self.offGroundTimer += 1
            else:
                self.offGroundTimer = 0

            # Friction
            if self.state != "moving" and (self.state != "sprinting" and self.stamina > 0) and self.state != "jumping":
                if self.spd > 0.25:
                    self.spd -= self.acc
                elif self.spd < -0.25:
                    self.spd += self.acc
                else:
                    self.spd = 0

            # Speed Cap
            self.speedCap()

            # Update Player Status
            self.updateStamina()
            self.updateHealth()
            if self.attackCooldown != 0:
                self.updateAttackCooldown()
            if self.iFrames > 0:
                self.iFrames -= 1

            # Set Default Values (state, onGround, timers...)
            self.maxSpd = 4
            self.onGround = False

            # Test New Position
            deltaPos = Position(int(self.spd), int(self.ySpd))

            # Enemy Collision
            for enemy in curLevel.enemiesList:
                if enemy.state == "moving" and enemy.variant != "Archer" and\
                        self.collision(deltaPos, [enemy], enemy.solid, True):
                    if self.iFrames <= 0:
                        self.health -= enemy.damage
                        enemy.stun = 45
                        self.iFrames = 20
                    self.handleKnockback(deltaPos)

                elif enemy.hurtbox.active and self.collision(deltaPos, [enemy.hurtbox], enemy.hurtbox.solid, True):
                    if self.iFrames <= 0:
                        self.health -= enemy.damage
                        self.iFrames = 20
                    self.handleKnockback(deltaPos)

                elif enemy.projectileList is not None:
                    for projectile in enemy.projectileList:
                        if PointRectCollision(self.pos, self.size, projectile.pos):
                            projectile.hit = True
                            if self.iFrames <= 0:
                                self.health -= enemy.damage
                                self.iFrames = 20

            # Tilemap Collision
            for chunk in curLevel.tilemap.chunks:
                if chunk.loaded:
                    self.collision(deltaPos, chunk.collisionTiles)

            # Set New Position
            self.pos += deltaPos

            # Camera
            curLevel.camera.setOffset(deltaPos)

            # Animate
            self.animate()

            # If Dead:
            if Globs.DEAD and self.size != self.defaultSize and self.pD:
                self.size = self.defaultSize
                self.pos.y -= self.size.h - self.duckSize.h
                self.pD = False

    # RENDER -----------------------------------------------------------------------------------------------------------
    def render(self, surface, camOffset):
        # Player
        tmp = self.pos + camOffset
        if Globs.DEBUG_GRAPHICS:
            if self.iFrames <= 0:
                pygame.draw.rect(surface, magenta, [tmp.x, tmp.y, self.size.w, self.size.h], 0)
            else:
                pygame.draw.rect(surface, white, [tmp.x, tmp.y, self.size.w, self.size.h])

        # Directional
        if self.state == "ducking" or self.state == "duck_attacking":
            tmp.y -= 24
        if self.LR == 'R':
            # Animation
            tmp.x -= 8
            surface.blit(Player.ImageDict[self.state], tmp.i, [int(self.curFrame) * 48, 0, 48, 48])
        else:
            image = Player.ImageDict[self.state]
            image = pygame.transform.flip(image, True, False)
            tmp.x -= 8
            surface.blit(image, tmp.i, [(Player.AnimationLengthDict[self.state] -
                                         int(self.curFrame) - 1) * 48, 0, 48, 48])

        # Hurtbox (DEBUG)
        if Globs.DEBUG_GRAPHICS:
            tmpbox = self.hurtbox.pos + camOffset
            if self.hurtbox.active:
                pygame.draw.rect(surface, red, [tmpbox.x, tmpbox.y, self.hurtbox.size.w, self.hurtbox.size.h], 1)

        # UI Elements
        # Health
        pygame.draw.rect(surface, black, [10, 10, self.maxSetHealth, 20], 0)
        pygame.draw.rect(surface, deepDarkRed, [11, 11, self.setHealth, 18], 0)
        pygame.draw.rect(surface, darkRed, [11, 11, self.health, 18], 0)
        surface.blit(Player.UIDict["H" + str(self.health >= self.maxSetHealth / 2)], (-2, 4))

        # Stamina
        pygame.draw.rect(surface, black, [10, 35, self.maxSetStamina, 20], 0)
        pygame.draw.rect(surface, deepDarkGreen, [11, 36, self.setStamina, 18], 0)
        pygame.draw.rect(surface, darkGreen, [11, 36, self.stamina, 18], 0)
        surface.blit(Player.UIDict["S" + str(self.stamina >= self.maxSetStamina / 2)], (0, 30))

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
        """deltaPos.x += self.takeKnockback.x
        deltaPos.y += self.takeKnockback.y
        self.takeKnockback.x = 0
        self.takeKnockback.y = 0"""

    def speedCap(self):
        if self.spd >= self.maxSpd:
            self.spd = self.maxSpd
        elif self.spd <= -self.maxSpd:
            self.spd = -self.maxSpd
        if self.ySpd >= self.yMaxSpd:
            self.ySpd = self.yMaxSpd
        elif self.ySpd <= -self.yMaxSpd:
            self.ySpd = -self.yMaxSpd

        if Globs.DEBUG_TEXT:
            print(" Player Speed = " + str(self.spd) + " " + str(self.ySpd))

    def updateStamina(self):
        if self.stamina < self.setStamina and self.staminaDrain <= 0:
            if self.state == "idle":
                self.stamina += 0.35
            elif self.state == "moving":
                self.stamina += 0.1
            if self.stamina < 0:
                self.stamina = 0
        elif self.stamina > self.setStamina:
            self.stamina = self.setStamina
        if self.staminaDrain > 0:
            self.stamina -= 0.5
            self.staminaDrain -= 0.5

        if self.stamina < self.setStamina:
            self.setStamina -= 0.005
            if self.stamina < 0:
                self.stamina = 0

    def updateHealth(self):
        if self.health <= 0:
            Globs.DEAD = True
            Globs.PAUSED = True
        if self.health < self.setHealth and self.healthDrain <= 0:
            if self.state == "idle":
                self.health += 0.1
            elif self.state == "moving":
                self.health += 0.05
        elif self.health > self.setHealth:
            self.health = self.setHealth
        if self.healthDrain > 0:
            self.health -= 0.5
            self.healthDrain -= 0.5

        if self.health < self.setHealth:
            self.setHealth -= 0.05

    def updateAttackCooldown(self):
        if self.attackCooldown > 0:
            self.attackCooldown -= 0.15
            if self.attackCooldown > 1:
                self.state = "attacking"
        elif self.attackCooldown < 0:
            self.attackCooldown = 0

    def generateHurtbox(self):
        self.hurtbox.active = True
        if self.LR == "L":
            self.hurtbox.pos.x = self.center.x - self.hurtbox.size.w
        else:
            self.hurtbox.pos.x = self.center.x
        if self.UD == "U":
            self.hurtbox.pos.y = self.center.y - self.hurtbox.size.h
        else:
            self.hurtbox.pos.y = self.center.y

    def animate(self):
        # Check State
        if self.offGroundTimer >= 4 and self.state != "attacking":
            self.state = 'jumping'
        if self.UD == "D" and self.state != "jumping":
            if self.state == "attacking":
                self.state = "duck_attacking"
            else:
                self.state = "ducking"

        if self.state != self.oldState:
            self.curFrame = 0
        self.oldState = self.state

        # Add Frames
        self.curFrame += Player.FrameLengthDict[self.state]

        # Loop
        if int(self.curFrame) >= Player.AnimationLengthDict[self.state]:
            self.curFrame = 0
