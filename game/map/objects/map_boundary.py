from pygame.math import Vector2

from .map_object import MapObject
from game.components.physics.foothold import Foothold
from game.components.physics.wall import Wall

class MapBoundary(MapObject):
    def __init__(self, size):
        super().__init__()
        self.size = size
    
    def create(self, world, mapdef):
        floor_left = Vector2(0, 0)
        floor_right = Vector2(self.size.x, 0)
        #TODO: an actual ceiling
        ceiling_left = Vector2(0, self.size.y)
        ceiling_right = self.size.copy()

        floor = world.create_entity([Foothold(floor_left, floor_right, allow_jump_down=False)])
        world.create_entity([Wall(floor_left, ceiling_left, 1)])
        world.create_entity([Wall(floor_right, ceiling_right, -1)])

        return floor