import pygame
from pygame.math import Vector2

from .action import Action
from game.components.physics.physics import Physics

#TODO: add physics method for jumping down so it can NOT, if the fh has jumping down disabled
class JumpDown(Action):
    def __init__(self):
        super().__init__()
    
    def start(self, entity):
        self.done = True
        phys = entity.get_component(Physics)

        jump_sound = pygame.mixer.Sound("game/assets/audio/jump.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(jump_sound)
        
        phys.dislodge(ignore_last_foothold=True)
        phys.apply_force(Vector2(0, 0.05))