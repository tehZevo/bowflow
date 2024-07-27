
class Component:
    def __init__(self):
        self.entity = None
        self.world = None

    def init(self):
        pass
    
    def update(self):
        pass

    def get_component(self, component_type):
        return self.entity.get_component(component_type)
    
    def for_each_component(self, component_type, f):
        self.entity.for_each_component(component_type, f)
