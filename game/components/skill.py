import pygame

from ..ecs import Component
from .position import Position

class Skill(Component):
    def __init__(self, skilleffect):
        super().__init__()
        self.skilleffect = skilleffect
        self.caster = None
        self.done = False
    
    def start(self):
        self.skilleffect.start(self)

    def update(self):
        self.skilleffect.update(self)

        if self.done:
            self.entity.remove()