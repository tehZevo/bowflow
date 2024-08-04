import random

from pygame.math import Vector2

from .map_object import MapObject
from game.components.physics.foothold import Foothold
from game.components.physics.rope import Rope
from game.components.spawner import Spawner

class FootholdStack(MapObject):
    def __init__(self, start_pos, size, n_platforms=2, ropes_per_platform=2, with_spawners=False):
        super().__init__()
        self.start_pos = start_pos
        self.size = size
        self.n_platforms = n_platforms
        self.ropes_per_platform = ropes_per_platform
        self.with_spawners = with_spawners
    
    def create(self, world, mapdef):
        #TODO: use mapdef to determine type of spawner
        diff = self.size.y / (self.n_platforms + 1)
        
        footholds = []
        for i in range(1, self.n_platforms + 1):
            start = self.start_pos + Vector2(0, diff * i)
            end = start + Vector2(self.size.x, 0)

            foothold = world.create_entity([
                Foothold(start, end),
                *([Spawner()] if self.with_spawners else []),
            ])
            footholds.append(foothold)

            for _ in range(self.ropes_per_platform):
                rope_pos = start + (end - start) * random.random()
                rope_length = diff / 2 + diff / 2 * random.random()
                rope = world.create_entity([Rope(rope_pos, rope_length)])
        
        return footholds