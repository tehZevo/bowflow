#TODO: subfeatures?

class MapFeature:
    def __init__(self):
        self.x = None
        self.y = None
        self.width = None
        self.height = None

    def set_bounds(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def try_place(self, layout, mapdef):
        """Try to place this feature in the map layout, if successful, mark map cells as occupied and set position/bounds"""
    
    def generate_entities(self, layout, world, mapdef):
        #TODO: generate ents
        raise NotImplementedError

    def generate_tiles(self, mapdef):
        #TODO: generate tiles
        raise NotImplementedError