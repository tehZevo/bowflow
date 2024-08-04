
class MapDef:
    def __init__(self, name, generator, mobdef=None):
        self.name = name
        self.generator = generator
        self.mobdef = mobdef
    
    def generate(self, world):
        self.generator(world, self)