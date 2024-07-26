import pygame
from pygame.math import Vector2

from .action import Action
from ..components import Physics

class Jump(Action):
    def __init__(self, power):
        super().__init__()
        self.power = power
    
    def start(self, entity):
        phys = entity.get_component(Physics)

        jump_sound = pygame.mixer.Sound("jump.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(jump_sound)
        
        phys.dislodge()
        phys.apply_force(Vector2(0, self.power))
        self.done = True