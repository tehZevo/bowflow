from .physics_state import PhysicsState

class GroundState(PhysicsState):
    def __init__(self, physics):
        super().__init__(physics)
    
    def update(self):
        raise NotImplementedError