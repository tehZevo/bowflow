import pygame

from ..ecs import Component
from .position import Position

class Skill(Component):
    """
    Represents an instance of a skill effect.
    Has a caster and optionally a target which is set by the UseSkill action or a target method.
    """
    
    def __init__(self, skilleffect):
        super().__init__()
        self.skilleffect = skilleffect
        self.caster = None
        self.target = None
        self.done = False
    
    def start(self):
        self.skilleffect.start(self)

    def update(self):
        self.skilleffect.update(self)

        if self.done:
            self.entity.remove()