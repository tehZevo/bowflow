
class PhysicsState:
    def __init__(self, physics):
        self.physics = physics
    
    def update(self):
        raise NotImplementedError