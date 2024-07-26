import pygame

from .skilleffect import SkillEffect

class Sound(SkillEffect):
    def __init__(self, sound_path):
        super().__init__()
        self.sound_path = sound_path
    
    def run(self, caster):
        sound = pygame.mixer.Sound(self.sound_path) #TODO: store this somewhere
        pygame.mixer.Sound.play(sound)