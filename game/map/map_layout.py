from collections import defaultdict
from enum import Enum

#TODO: this might need to be more than an enum.. eg solid or not, can_stand.. etc
CellFeature = Enum("CellFeature", "PLATFORM WALL ROPE PORTAL")

class MapLayout:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #each cell stores a set of cell features, this allows other map features to query (eg placing portal on foothold)
        self.cells = defaultdict(set)
        self.features = []
    
    def is_in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def get_cell(self, x, y):
        return self.cells[(x, y)]
    
    def find(self, cell_feature):
        return [k for k, v in self.cells.items() if cell_feature in v]
    
    def is_empty(self, x, y, width=1, height=1):
        for xx in range(x, x + width):
            for yy in range(y, y + height):
                if not self.is_in_bounds(xx, yy):
                    return False
                if len(self.cells[(xx, yy)]) != 0:
                    return False
        return True
    
    #TODO: a way to flag cells as having certain sub-features such as rope or foothold/platform
    #TODO: that or make features have parents
    def set_cell(self, x, y, cell_feature):
        self.cells[(x, y)].add(cell_feature)
    
    def set_cells(self, x, y, width, height, cell_feature):
        for xx in range(x, x + width):
            for yy in range(y, y + height):
                self.set_cell(xx, yy, cell_feature)
        