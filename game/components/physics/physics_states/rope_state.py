from .physics_state import PhysicsState

class RopeState(PhysicsState):
    def __init__(self, physics):
        super().__init__(physics)
    
    def update(self):
        raise NotImplementedError