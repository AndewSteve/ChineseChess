import pygame
import os

Sound_Asset_path = './Resource/sound'

class Mixer:
    def __init__(self):
        pygame.mixer.init()
        self.sound_dict:[str,pygame.mixer.Sound]={}
        self.initResource()

    def initResource(self):
        for filename in os.listdir(Sound_Asset_path):
            if filename.endswith(".mp3"):
                sound_name = os.path.splitext(filename)[0]
                sound_path = os.path.join(Sound_Asset_path,filename)
                sound = pygame.mixer.Sound(sound_path)
                self.sound_dict[sound_name] = sound
        

    def play(self,sound_name:str):
        if self.sound_dict.__contains__(sound_name):
            sound = self.sound_dict[sound_name]
            pygame.mixer.Sound.play(sound)
        else:
            print(f"未找到声源：{sound_name}")

