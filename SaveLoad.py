from EnemyVariants import SetEnemy, Projectile


# Save Game
def SaveGame(curLevel, saveLocation):
    print(saveLocation[23:-4])
    player = curLevel.player
    with open(saveLocation, 'w') as file:
        # Level
        file.write("LevelNumber=" + str(curLevel.num) + "\n")
        file.write("LevelEnemyCount=" + str(len(curLevel.enemiesList)) + "\n")
        # Camera
        file.write("CameraOffset=" + str(curLevel.camera.offset.i) + "\n")
        # Player
        file.write("PlayerPosition=" + str(player.pos.i) + "\n")
        file.write("PlayerSize=" + str(player.size.i) + "\n")
        file.write("PlayerSpeed=" + str(player.spd) + "\n")
        file.write("PlayerYSpeed=" + str(player.ySpd) + "\n")
        file.write("PlayerOnGround=" + str(player.onGround) + "\n")
        file.write("PlayerHasControl=" + str(player.hasControl) + "\n")
        file.write("PlayerState=" + str(player.state) + "\n")
        file.write("PlayerLR=" + str(player.LR) + "\n")
        file.write("PlayerUD=" + str(player.UD) + "\n")
        file.write("PlayerPD=" + str(player.pD) + "\n")
        file.write("PlayerHealth=" + str(player.health) + "\n")
        file.write("PlayerSetHealth=" + str(player.setHealth) + "\n")
        file.write("PlayerStamina=" + str(player.stamina) + "\n")
        file.write("PlayerSetStamina=" + str(player.setStamina) + "\n")
        file.write("PlayerStaminaDrain=" + str(player.staminaDrain) + "\n")
        file.write("PlayerHealthDrain=" + str(player.healthDrain) + "\n")
        file.write("PlayerAttackCooldown=" + str(player.attackCooldown) + "\n")
        file.write("PlayeriFrames=" + str(player.iFrames) + "\n")

        for i in range(len(curLevel.enemiesList)):
            enemy = curLevel.enemiesList[i]
            file.write("Enemy" + str(i) + "Position=" + str(enemy.pos.i) + "\n")
            file.write("Enemy" + str(i) + "Variant=" + str(enemy.variant) + "\n")
            file.write("Enemy" + str(i) + "Speed=" + str(enemy.spd) + "\n")
            file.write("Enemy" + str(i) + "YSpeed=" + str(enemy.ySpd) + "\n")
            file.write("Enemy" + str(i) + "OnGround=" + str(enemy.onGround) + "\n")
            file.write("Enemy" + str(i) + "State=" + str(enemy.state) + "\n")
            file.write("Enemy" + str(i) + "LR=" + str(enemy.LR) + "\n")
            file.write("Enemy" + str(i) + "UD=" + str(enemy.UD) + "\n")
            file.write("Enemy" + str(i) + "Health=" + str(enemy.health) + "\n")
            if enemy.projectileList is not None:
                file.write("Enemy" + str(i) + "ProjectileListLength=" + str(len(enemy.projectileList)) + "\n")
            else:
                file.write("Enemy" + str(i) + "ProjectileListLength=" + str(None) + "\n")
            if enemy.projectileList is not None:
                for x in range(len(enemy.projectileList)):
                    file.write("Enemy" + str(i) + "Projectile" + str(x) + "Position=" + str(
                        enemy.projectileList[x].pos.i) + "\n")
                    file.write("Enemy" + str(i) + "Projectile" + str(x) + "Target=" + str(
                        enemy.projectileList[x].targetPos.i) + "\n")
            file.write("Enemy" + str(i) + "HealthDrain=" + str(enemy.healthDrain) + "\n")
            file.write("Enemy" + str(i) + "AttackCooldown=" + str(enemy.attackCooldown) + "\n")
            file.write("Enemy" + str(i) + "SetAttackCooldown=" + str(enemy.setAttackCooldown) + "\n")
            file.write("Enemy" + str(i) + "Stun=" + str(enemy.stun) + "\n")
            file.write("Enemy" + str(i) + "iFrames=" + str(enemy.iFrames) + "\n")
            file.write("Enemy" + str(i) + "ActionTimer=" + str(enemy.actionTimer) + "\n")
        file.close()


# Load Game
def LoadGame(curLevel, fileLocation):
    readFile = open(fileLocation)
    lines = readFile.readlines()
    readFile.close()

    # Outside Loop Variables
    enemyCount = 0
    tempOffset = (0, 0)
    player = curLevel.player
    enemy = None

    position = (0, 0)
    projectilePosition = (0, 0)
    projectileListLength = 0

    for line in lines:
        line = line.strip()
        key, value = line.split("=")

        # Overwrite Current Data
        # Level
        if key == "LevelNumber":
            curLevel.loadLevel(int(value))
            curLevel.enemiesList = []
        elif key == "LevelEnemyCount":
            enemyCount = int(value)
        # Camera
        elif key == "CameraOffset":
            value = value[1:-1]
            tempOffset = tuple(map(int, value.split(",")))
        # Player
        elif key == "PlayerPosition":
            value = value[1:-1]
            player.setPosition(tuple(map(float, value.split(","))), curLevel.camera, True)
        elif key == "PlayerSize":
            value = value[1:-1]
            player.setSize(tuple(map(int, value.split(","))))
        elif key == "PlayerSpeed":
            player.spd = int(value)
        elif key == "PlayerYSpeed":
            player.ySpd = float(value)
        elif key == "PlayerOnGround":
            player.onGround = bool(value)
        elif key == "PlayerHasControl":
            player.hasControl = bool(value)
        elif key == "PlayerState":
            player.state = value
        elif key == "PlayerLR":
            player.LR = value
        elif key == "PlayerUD":
            player.UD = value
        elif key == "PlayerPD":
            player.pD = bool(value)
        elif key == "PlayerHealth":
            player.health = float(value)
        elif key == "PlayerSetHealth":
            player.setHealth = float(value)
        elif key == "PlayerStamina":
            player.stamina = float(value)
        elif key == "PlayerSetStamina":
            player.setStamina = float(value)
        elif key == "PlayerStaminaDrain":
            player.staminaDrain = float(value)
        elif key == "PlayerHealthDrain":
            player.healthDrain = float(value)
        elif key == "PlayerAttackCooldown":
            player.attackCooldown = float(value)
        elif key == "PlayeriFrames":
            player.iFrames = float(value)
        else:
            # Enemies
            for i in range(enemyCount):
                if key == "Enemy" + str(i) + "Position":
                    value = value[1:-1]
                    position = (tuple(map(int, value.split(","))))
                elif key == "Enemy" + str(i) + "Variant":
                    curLevel.enemiesList.append(SetEnemy(position, value))
                    enemy = curLevel.enemiesList[i]
                elif key == "Enemy" + str(i) + "Speed":
                    enemy.spd = float(value)
                elif key == "Enemy" + str(i) + "YSpeed":
                    enemy.ySpd = float(value)
                elif key == "Enemy" + str(i) + "OnGround":
                    enemy.onGround = bool(value)
                elif key == "Enemy" + str(i) + "State":
                    enemy.state = value
                elif key == "Enemy" + str(i) + "LR":
                    enemy.LR = value
                elif key == "Enemy" + str(i) + "UD":
                    enemy.UD = value
                elif key == "Enemy" + str(i) + "Health":
                    enemy.health = float(value)
                elif key == "Enemy" + str(i) + "ProjectileListLength":
                    if value == str(None):
                        projectileListLength = 0
                    else:
                        projectileListLength = int(value)
                        enemy.projectileList = []
                for x in range(projectileListLength):
                    if key == "Enemy" + str(i) + "Projectile" + str(x) + "Position":
                        value = value[1:-1]
                        projectilePosition = (tuple(map(int, value.split(","))))
                    if key == "Enemy" + str(i) + "Projectile" + str(x) + "Target":
                        value = value[1:-1]
                        # enemy.projectileList.append(Projectile(projectilePosition, tuple(map(int, value.split(",")))))
                        enemy.projectileList.append(Projectile(projectilePosition, player.center.i))
                if key == "Enemy" + str(i) + "HealthDrain":
                    enemy.healthDrain = float(value)
                elif key == "Enemy" + str(i) + "AttackCooldown":
                    enemy.attackCooldown = float(value)
                elif key == "Enemy" + str(i) + "SetAttackCooldown":
                    enemy.attackCooldown = float(value)
                elif key == "Enemy" + str(i) + "Stun":
                    enemy.stun = float(value)
                elif key == "Enemy" + str(i) + "iFrames":
                    enemy.iFrames = float(value)
                elif key == "Enemy" + str(i) + "ActionTimer":
                    enemy.actionTimer = float(value)
