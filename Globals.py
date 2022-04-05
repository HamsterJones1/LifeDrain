import pygame


class Globs:
    # Game State Variables
    RUNNING = True
    WIN = False
    DEBUG_TEXT = False
    DEBUG_GRAPHICS = False
    MASTER_VOLUME = True
    SOUND_EFFECTS = True
    MUSIC = True
    PAUSED = True

    # Display Variables
    MONITOR_SIZE = None
    WINDOW_SIZE = (800, 600)
    DISPLAY_SIZE = (800, 600)
    VIEW_SIZE = (400, 300)
    RENDER_DISTANCE = (VIEW_SIZE[0] * 1.7, VIEW_SIZE[1] * 1.75)
    DISPLAY_OFFSET = (0, 0)
    DISPLAY_RATIO = (4, 3)
    VIEW_SCALE = 2
    FULLSCREEN = False
    DISPLAY_RESIZABLE = False

    # Time Variables
    Clock = pygame.time.Clock()
    FPS = 60
    dt = 0

    # Player Variables
    DEAD = False

    # Tilemap Variables
    TILE_SIZE = 32  # Number of Pixels per row/col
    CHUNK_SIZE = 8  # Number of Tiles per  row/col

    # Game Mechanics Variables
    GRAVITY_ACC = 0.5
    GRAVITY_MAX = 30

    # Saves
    SAVE_FILES = []

    # Credits ( Also in Audio.py )
    # Music @ https://www.chosic.com/free-music/all/
    # Music_A: Komiku - Bicycle             @ https://www.chosic.com/free-music/all/?keyword=Komiku&artist
    # Music_B: Komiku - We need a plan      @ https://www.chosic.com/download-audio/24589/
    # Music_C: Monplaisir - Level 1         @ https://www.chosic.com/download-audio/24733/


# Window Resize Function
def ResizeWindow(dX, dY):
    pass


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
teal = (0, 255, 255)
blue = (0, 100, 255)
magenta = (255, 0, 255)
purple = (130, 0, 255)

lightGrey = (200, 200, 200)
lightBlue = (0, 200, 255)

darkRed = (200, 0, 0)
darkGreen = (0, 200, 30)

deepDarkRed = (100, 0, 0)
deepDarkGreen = (0, 80, 10)
