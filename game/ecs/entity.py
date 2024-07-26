
class Entity:
    def __init__(self):
        self.components = []
        self.world = None

    def add_component(self, component):
        component.entity = self
        component.world = self.world
        self.components.append(component)
        component.init()
    
    def remove(self):
        self.world.remove_entity(self)
    
    def get_component(self, component_type):
        #TODO: what if duplicates or different subclasses?
        matches = [c for c in self.components if isinstance(c, component_type)]
        if len(matches) > 0:
            return matches[0]
        
        return None
            
    def update(self):
        for component in self.components:
            component.update()