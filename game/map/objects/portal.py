import random
from pygame.math import Vector2

from .map_feature import MapFeature
from game.components.physics.foothold import Foothold
from game.components.physics.position import Position
from game.components.physics.rope import Rope
from game.components.physics.wall import Wall
from game.map.map_layout import CellFeature
from game.components.portal import Portal as PortalComponent

class Portal(MapFeature):
    def __init__(self):
        super().__init__()
        self.pos = None
    
    def try_place(self, layout, mapdef):
        platforms = layout.find(CellFeature.PLATFORM)
        random.shuffle(platforms)
        print(len(platforms))
        for x, y in platforms:
            if layout.is_empty(x, y + 1):
                layout.set_cell(x, y + 1, CellFeature.PORTAL)
                self.pos = Vector2(x, y + 1)
                self.set_bounds(x, y + 1, 1, 1)
                return True
        
        return False
    
    def generate_entities(self, layout, world, mapdef):
        from game.map.seaside_city import seaside_city

        #TODO: where to get portal destination from?
        portal = world.create_entity([PortalComponent(seaside_city)])
        portal.get_component(Position).set_pos(self.pos + Vector2(0.5, -1)) #TODO: check offsets
        
    def generate_tiles(self, mapdef):
        #TODO: generate tiles
        pass