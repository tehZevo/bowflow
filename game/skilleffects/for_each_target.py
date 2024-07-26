import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from ..components.position import Position
from ..components.monster import Monster
from ..components.actor import Actor
from ..utils import point_in_aabb
from ..components.skill import Skill

from ..constants import DEBUG_TARGETS

class ForEachTarget(SkillEffect):
    def __init__(self, in_a, apply=[]):
        super().__init__()
        self.method = in_a
        self.effects = apply
    
    def start(self, skill):
        if DEBUG_TARGETS:
            self.method.debug(skill.caster)
            
        targets = self.method.get_targets(skill.caster)

        for target in targets:
            for effect in self.effects:
                skill_comp = Skill(effect)
                skill_comp.caster = skill.caster
                skill_comp.target = target
                skill.world.create_entity([skill_comp])
                #TODO: do we need to have a start method or can we rely on init from component?
                skill_comp.start()