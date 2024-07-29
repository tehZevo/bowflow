
class PhysicsStateListener:
    def __init__(self):
        super().__init__()
    
    def on_physics_state_changed(self, state):
        raise NotImplementedError