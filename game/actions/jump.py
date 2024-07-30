import pygame
from pygame.math import Vector2

from .action import Action
from game.components.physics.physics import Physics

class Jump(Action):
    def __init__(self, power):
        super().__init__()
        self.power = power
    
    def start(self, entity):
        self.done = True
        phys = entity.get_component(Physics)

        jump_sound = pygame.mixer.Sound("game/assets/audio/jump.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(jump_sound)
        
        phys.dislodge()
        phys.apply_force(Vector2(0, self.power))