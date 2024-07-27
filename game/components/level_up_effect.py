import pygame
from pygame.math import Vector2

from ..ecs.component import Component
from .effect import Effect
from .position import Position
from .sprite import Sprite

class LevelUpEffect(Component):
    """Level up effect for the given entity"""
    def __init__(self, for_entity):
        super().__init__()
        self.for_entity = for_entity
    
    def init(self):
        pos = self.for_entity.get_component(Position).pos
        pos = pos + Vector2(0, 2)

        self.entity.add_component(Position(pos))
        self.entity.add_component(Sprite())
        self.entity.add_component(Effect("game/assets/images/level_up.png", time=1))