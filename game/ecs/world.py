from .entity import Entity

class World:
    def __init__(self):
        self.entities = []
    
    def create_entity(self, components=[]):
        entity = Entity()
        entity.world = self
        for c in components:
            entity.add_component(c)
        self.entities.append(entity)
        
        return entity

    def get_all_components(self, component_type):
        comps = []
        for entity in self.entities:
            for component in entity.components:
                if isinstance(component, component_type):
                    comps.append(component)
        return comps

    def update(self):
        for entity in self.entities.copy():
            entity.update()
        
        self.entities = [e for e in self.entities if e.alive]