import pygame
from Globals import Globs
from Text import Text


# Credits
# Music @ https://www.chosic.com/free-music/all/
# Music_A: Komiku - Bicycle             @ https://www.chosic.com/free-music/all/?keyword=Komiku&artist
# Music_B: Komiku - We need a plan      @ https://www.chosic.com/download-audio/24589/
# Music_C: Monplaisir - Level 1         @ https://www.chosic.com/download-audio/24733/


class Audio:
    creditDict = {"Assets/Audio/Music/Komiku_-_12_-_Bicycle.mp3": " music: komiku - bicycle",
                  "Assets/Audio/Music/Komiku_-_02_-_We_need_a_plan.mp3": " music: komiku - we need a plan",
                  "Assets/Audio/Music/Monplaisir_-_04_-_Level_1.mp3": " music: monplaisir - level 1"}

    def __init__(self):
        self.music = "Assets/Audio/Music/Komiku_-_12_-_Bicycle.mp3"
        self.playMusic = True
        self.credit = Text(Audio.creditDict[self.music], (0, 292), 8)
        self.loadMusic()

    def loadMusic(self, file=None, loop=-1, volume=None):
        if Globs.MASTER_VOLUME and Globs.MUSIC:
            if file is not None:
                self.music = file
            pygame.mixer.music.load(self.music)
            self.credit.updateText(Audio.creditDict[self.music])

            if volume is not None:
                pygame.mixer.music.set_volume(volume)

            pygame.mixer.music.play(loop)
            self.playMusic = True

    def pause(self):
        self.playMusic = False
        pygame.mixer.music.stop()

    def play(self, loop=-1):
        self.playMusic = True
        pygame.mixer.music.play(loop)

