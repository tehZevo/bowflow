from collections import defaultdict

class MapLayout:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = defaultdict(lambda: None)
        self.features = []
    
    def is_in_bounds(self, x, y):
        print(x, y)
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def get_cell(self, x, y):
        return self.cells[(x, y)]
    
    def is_empty(self, x, y, width=1, height=1):
        for xx in range(x, x + width):
            for yy in range(y, y + height):
                if not self.is_in_bounds(xx, yy):
                    return False
                if self.cells[(xx, yy)] is not None:
                    return False
        return True
    
    #TODO: a way to flag cells as having certain sub-features such as rope or foothold/platform
    #TODO: that or make features have parents
    def set_cell(self, x, y, feature):
        self.cells[(x, y)] = feature
    
    def set_cells(self, x, y, width, height, feature):
        for xx in range(x, x + width):
            for yy in range(y, y + height):
                self.set_cell(xx, yy, feature)
        