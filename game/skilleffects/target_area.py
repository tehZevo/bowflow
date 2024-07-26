import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from ..components.position import Position
from ..components.monster import Monster
from ..components.actor import Actor
from ..utils import point_in_aabb

class TargetArea(SkillEffect):
    def __init__(self, offset, size):
        super().__init__()
        self.offset = offset
        self.size = size
    
    def run(self, caster):
        caster_pos = caster.get_component(Position).pos
        caster_dir = caster.get_component(Actor).facing_dir
        area_pos = caster_pos + self.offset
        area_min = area_pos - self.size / 2
        area_max = area_pos + self.size / 2

        mobs = caster.world.get_all_components(Monster)
        
        #filter to target area
        mobs = [mob for mob in mobs if point_in_aabb(
            mob.get_component(Position).pos,
            area_min,
            area_max
        )]

        #TODO: how to store targets for next skill effect?
        #TODO: rename this to "with target area" and call children with targets?
        #or do we store "Targets" component on an entity?
        #or do we create one entity for each target and then replicate the child skill effect for each?
