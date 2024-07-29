
class Component:
    def __init__(self):
        self.entity = None
        self.world = None
        self.requirements = []

    def ensure_requirements(self):
        for Req in self.requirements:
            if self.entity.get_component(Req) is None:
                req = Req()
                self.entity.add_component(req)

    def init(self):
        pass
    
    def update(self):
        pass

    def get_component(self, component_type):
        return self.entity.get_component(component_type)
    
    def for_each_component(self, component_type, f):
        self.entity.for_each_component(component_type, f)
