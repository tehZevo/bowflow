
class Component:
    def __init__(self):
        self.entity = None
        self.world = None

    def update(self):
        pass

    def get_component(self, component_type):
        return self.entity.get_component(component_type)
