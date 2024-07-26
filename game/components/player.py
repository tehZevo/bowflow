import pygame

from ..ecs.component import Component
from .position import Position
from .physics import Physics
from .actor import Actor
from ..actions import Move, Jump, UseSkill
from ..skills import leap

class Player(Component):
    def __init__(self):
        super().__init__()

    def update(self):
        keys = pygame.key.get_pressed()
        
        x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        
        #TODO: only jump on press (make hold not jump so player has to time it?)
        jump = keys[pygame.K_c]

        phys = self.get_component(Physics)
        pos = self.get_component(Position)

        actor = self.get_component(Actor)

        if not phys.on_ground and keys[pygame.K_d] and actor.action == None:
            actor.act(UseSkill(leap))
        
        if phys.on_ground and jump:
            actor.act(Jump(0.15))
        
        if phys.on_ground and x != 0:
            actor.act(Move(x / 100))
            