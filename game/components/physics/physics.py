import random

from pygame.math import Vector2

from game.ecs import Component
from .position import Position
from .physics_state_listener import PhysicsStateListener
from .physics_states.air_state import AirState
from .physics_states.ground_state import GroundState
from .physics_states.rope_state import RopeState

class Physics(Component):
    def __init__(self):
        super().__init__()

        self.state = AirState(self)
        
        self.stay_on_footholds = False

        self.requirements = [Position]
        self.prevent_updates = False
    
    @property
    def on_ground(self):
        return type(self.state) == GroundState
    
    @property
    def in_air(self):
        return type(self.state) == AirState
    
    @property
    def on_rope(self):
        return type(self.state) == RopeState

    #TODO: change this so if no pos provided, projects position onto foothold
    def move_to_foothold(self, fh, foothold_pos=None):
        #TODO: enter a ground state
        self.state = GroundState(self)
        self.state.foothold = fh
        self.state.foothold_pos = foothold_pos if foothold_pos is not None else random.random()
        self.state.update_pos()

        self.alert_listeners()

    def alert_listeners(self):
        for listener in self.entity.get_all_components(PhysicsStateListener):
            listener.on_physics_state_changed(self.state)

    def apply_force(self, force):
        match self.state:
            case AirState():
                self.state.force += force
            case GroundState():
                self.state.force += force.x
            case RopeState():
                self.state.vel += force.y

    def dislodge(self, keep_vel=True, ignore_last_foothold=False):
        """Detatch from foothold"""
        if not self.on_ground:
            return

        vel = Vector2()
        if keep_vel:
            vel = Vector2(self.state.vel, 0)
        
        ignored_footholds = [self.state.foothold] if ignore_last_foothold else []
        self.state = AirState(self, ignored_footholds=ignored_footholds)
        self.state.vel = vel

        self.alert_listeners()
    
    def grab_rope(self, rope):
        self.state = RopeState(self)
        pos = self.get_component(Position).pos
        rope_pos = (pos - rope.bottom).dot(rope.top - rope.bottom) / (rope.top - rope.bottom).length_squared()
        self.state.rope = rope
        self.state.rope_pos = rope_pos

        self.alert_listeners()
    
    def drop_from_rope(self, direction=0):
        vel = Vector2() if direction == 0 else Vector2(direction, 1.5) / 15 #TODO: test vel
        self.state = AirState(self)
        self.state.vel = vel

        self.alert_listeners()

    def zero_velocity(self):
        match self.state:
            case AirState():
                self.state.vel = Vector2()
            case GroundState():
                self.state.vel = 0
            case RopeState():
                self.state.vel = 0

    def update(self):
        #TODO: allow transitioning between multiple states per frame?
        
        if self.prevent_updates:
            return

        self.state.update()
        