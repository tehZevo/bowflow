import random
from pygame.math import Vector2

from .map_feature import MapFeature
from game.components.physics.foothold import Foothold
from game.components.physics.rope import Rope
from game.components.physics.wall import Wall
from game.map.map_layout import CellFeature

class Platform(MapFeature):
    def __init__(self):
        super().__init__()
        #TODO: create position and size at creation time, that way we can have
        #- small platform
        #- medium platform
        #- large platform (all extends platform)
        #- and manual platform (specify location) (TODO: how to specify if we pass CLASSES?) lambda?
        self.platform_start = None
        self.platform_end = None
        self.rope_pos = None
        self.rope_length = None
    
    def try_place(self, layout, mapdef):
        MIN_LENGTH = 2
        MAX_LENGTH = 10
        length = random.randint(MIN_LENGTH, MAX_LENGTH + 1)
        x = random.randint(0, layout.width - length)
        y = random.randint(0, layout.height - 1)

        if not layout.is_empty(x, y, length, 1):
            return False
        
        self.platform_start = Vector2(x, y)
        self.platform_end = Vector2(x + length, y)

        #TODO: place a rope until it hits something
        rope_start = random.randint(x, x + length - 1)
        rope_length = 0
        while True:
            if layout.is_empty(rope_start, y - rope_length):
                rope_length += 1
            else:
                break
        #back off a bit
        rope_length -= random.randint(1, 2)

        if rope_length > 0:
            self.rope_pos = Vector2(rope_start + 0.5, y)
            self.rope_length = rope_length
        
        #TODO: try to place a rope until it hits a platform, specifically

        layout.set_cells(x, y, length, 1, CellFeature.PLATFORM)
        layout.set_cells(rope_start, y - rope_length, 1, rope_length, CellFeature.ROPE)

        #TODO: include rope in bounds
        self.set_bounds(x, y, length, 1)

        return True
    
    def generate_entities(self, layout, world, mapdef):
        world.create_entity([Foothold(self.platform_start, self.platform_end)])
        if self.rope_pos is not None:
            world.create_entity([Rope(self.rope_pos, self.rope_length)])

    def generate_tiles(self, mapdef):
        #TODO: generate tiles
        pass