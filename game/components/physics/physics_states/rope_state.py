from ..position import Position
from .physics_state import PhysicsState

class RopeState(PhysicsState):
    def __init__(self, physics):
        super().__init__(physics)
        self.rope = None
        self.rope_pos = None
        #rope state has no force, vel is applied to pos and then reset
        self.vel = 0
    
    def update_pos(self):
        pos = self.rope.bottom + (self.rope.top - self.rope.bottom) * self.rope_pos
        self.physics.get_component(Position).set_pos(pos)

    def update(self):
        pos = self.physics.get_component(Position)

        # #if we reach top of rope, drop off to air state
        rope_length = abs(self.rope.top.y - self.rope.bottom.y)
        
        #TODO: check math
        print(self.vel)
        self.rope_pos = self.rope_pos + self.vel / rope_length
        self.vel = 0

        self.update_pos()

        if self.rope_pos > 1 or self.rope_pos < 0:
            self.physics.drop_from_rope()