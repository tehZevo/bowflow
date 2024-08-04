import random

from pygame.math import Vector2

from .map_object import MapObject
from game.components.physics.foothold import Foothold
from game.components.physics.rope import Rope
from game.components.spawner import Spawner

class FootholdChain(MapObject):
    def __init__(self, points, n_platforms=2, ropes_per_platform=2, with_spawners=False):
        super().__init__()
        self.points = points
        if len(points) < 2:
            raise ValueError("Please provide more than 2 points.")
    
    def create(self, world, mapdef):
        #TODO: use mapdef to determine type of spawner
        start = self.points[0]
        footholds = []

        last_foothold = None
        
        for end in self.points[1:]:
            fh_comp = Foothold(start, end)

            if last_foothold is not None:
                fh_comp.prev = last_foothold
                last_foothold.next = fh_comp

            foothold = world.create_entity([fh_comp])
            last_foothold = fh_comp
            footholds.append(foothold)
            
            start = end
        
        return footholds