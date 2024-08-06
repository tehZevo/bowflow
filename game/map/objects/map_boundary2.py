from pygame.math import Vector2

from .map_feature import MapFeature
from game.components.physics.foothold import Foothold
from game.components.physics.wall import Wall
from game.map.map_layout import CellFeature

#TODO: floor/wall/ceiling thickness
class MapBoundary(MapFeature):
    def __init__(self):
        super().__init__()
        self.floor = None
        self.walls = None
    
    def try_place(self, layout, mapdef):
        width = layout.width
        height = layout.height

        floor = (0, 0, width - 1, 1)
        left_wall = (0, 0, 1, height - 1)
        right_wall = (width - 1, 0, 1, height - 1)
        
        if not layout.is_empty(*floor) \
            or not layout.is_empty(*left_wall) \
            or not layout.is_empty(*right_wall):
            return False
        
        self.floor = floor
        self.walls = [left_wall, right_wall]

        #TODO: change to cellfeatures
        layout.set_cells(*floor, CellFeature.PLATFORM)
        layout.set_cells(*left_wall, CellFeature.WALL)
        layout.set_cells(*right_wall, CellFeature.WALL)

        self.set_bounds(0, 0, width, height)

        return True
    
    def generate_entities(self, layout, world, mapdef):
        floor_left = Vector2(self.x, self.y)
        floor_right = Vector2(self.x + self.width, self.y)
        left_wall_top = Vector2(self.x, self.y + self.height)
        right_wall_top = Vector2(self.x + self.width, self.y + self.height)
        world.create_entity([Foothold(floor_left, floor_right)])
        world.create_entity([Wall(floor_left, left_wall_top)])
        world.create_entity([Wall(floor_right, right_wall_top)])

    def generate_tiles(self, mapdef):
        #TODO: generate tiles
        pass