import pygame
from pygame.math import Vector2

from ...components.position import Position
from ...components.monster import Monster
from ...components.actor import Actor
from ...components.debug_box import DebugBox
from ...utils import point_in_aabb
from ...constants import PPU

from .target_method import TargetMethod

class TargetBox(TargetMethod):
    def __init__(self, offset, size, max_targets=10):
        super().__init__()
        self.offset = offset
        self.size = size
        self.max_targets = max_targets
    
    def debug(self, caster):
        min, max = self.get_bounds(caster)
        caster.world.create_entity([
            DebugBox(min, max)
        ])

    def get_bounds(self, caster):
        caster_pos = caster.get_component(Position).pos
        caster_dir = caster.get_component(Actor).facing_dir
        area_pos = caster_pos + self.offset.elementwise() * Vector2(caster_dir, 1)
        area_min = area_pos - self.size / 2
        area_max = area_pos + self.size / 2

        return area_min, area_max

    def get_targets(self, caster):
        min, max = self.get_bounds(caster)

        mobs = caster.world.get_all_components(Monster)
        
        #filter to target area
        mobs = [mob for mob in mobs if point_in_aabb(
            mob.get_component(Position).pos,
            min,
            max
        )]

        #TODO: sort by distance to caster

        #restrict to max targets
        mobs = mobs[:self.max_targets]

        return mobs
