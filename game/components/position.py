from pygame.math import Vector2

from ..ecs.component import Component

class Position(Component):
    def __init__(self, pos=None):
        super().__init__()

        self.pos = pos if pos is not None else Vector2()
    
    def set_pos(self, pos):
        self.pos = pos