import pygame
from Globals import *
from PositionVector import Position as Pos, Size


class Tile:
    def __init__(self, position, textureKey, collision, damage):
        self.pos = Pos(*position)
        self.size = Size(Globs.TILE_SIZE, Globs.TILE_SIZE)
        self.texKey = textureKey
        self.collision = collision  # N-None, A-All, T-Top, B-Bottom, L-Left, R-Right
        self.damage = damage


class Chunk:
    def __init__(self, position):
        self.loaded = True
        self.tiles = []
        self.collisionTiles = []
        self.pos = Pos(*position)

    def setCollisionTiles(self):
        for tile in self.tiles:
            if tile.collision != "N":
                self.collisionTiles.append(tile)


class Tilemap:
    def __init__(self, fileName):
        self.mapSize = None
        self.textures = {}
        self.collisionTiles = {}
        self.damageTiles = {}
        self.allTiles = []
        self.chunks = []

        self.map = self.tilemapFromFile(fileName)
        for chunk in self.chunks:
            chunk.setCollisionTiles()

    def tilemapFromFile(self, fileName):
        readFile = open(fileName, "r")
        lines = readFile.readlines()
        readFile.close()
        mapString = ""
        for line in lines:
            key, value = line.split("=")
            if key == "mapLine":
                mapString += value[1:-1]
                mapString += "\n"
            elif key == "loadTexture":
                textureKey, textureFileName, collision, damage = value.split(",")
                tex = pygame.image.load(textureFileName)
                self.textures[textureKey] = pygame.transform.scale(tex, (Globs.TILE_SIZE, Globs.TILE_SIZE))
                self.collisionTiles[textureKey] = collision
                self.damageTiles[textureKey] = damage
            elif key == "mapSize":
                w, h = value.split(",")
                self.mapSize = (int(w), int(h))

        self.generateChunks()
        return self.tilemapFromString(mapString.strip())

    def tilemapFromString(self, mapString):
        localTilemap = []
        for i in range(self.mapSize[1]):
            localTilemap.append(["  "] * self.mapSize[0])
        lines = mapString.split("\n")
        row = 0
        for line in lines:
            for col in range(self.mapSize[0]):
                tmpKey = line[col * 2: col * 2 + 2]
                localTilemap[row][col] = tmpKey
                if tmpKey != "  " and tmpKey != "":
                    x = Globs.TILE_SIZE * col
                    y = Globs.TILE_SIZE * row
                    for chunk in self.chunks:
                        if x <= chunk.pos.x + Globs.CHUNK_SIZE * Globs.TILE_SIZE:
                            if y <= chunk.pos.y + Globs.CHUNK_SIZE * Globs.TILE_SIZE:
                                chunk.tiles.append(Tile((x, y), tmpKey, self.collisionTiles[tmpKey], self.damageTiles[tmpKey]))
                                break
            row += 1

        return localTilemap

    def generateChunks(self):
        for i in range(self.mapSize[0] // Globs.CHUNK_SIZE + 1):
            x = i * (Globs.CHUNK_SIZE * Globs.TILE_SIZE)
            for j in range(self.mapSize[1] // Globs.CHUNK_SIZE + 1):
                y = j * (Globs.CHUNK_SIZE * Globs.TILE_SIZE)
                self.chunks.append(Chunk((x, y)))

    def render(self, surface, camOffset):
        for chunk in self.chunks:
            if chunk.loaded:
                for tile in chunk.tiles:
                    surface.blit(self.textures[tile.texKey], (tile.pos + camOffset).i)
