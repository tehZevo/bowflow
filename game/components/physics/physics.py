#TODO: clean up imports
import random

from pygame.math import Vector2

from game.ecs import Component
from game.utils import intersect, project_onto_foothold
from game.constants import GRAVITY, GROUND_FRICTION, AIR_FRICTION
from .position import Position
from .foothold import Foothold
from .wall import Wall
from .physics_states.air_state import AirState
from .physics_states.ground_state import GroundState
from .physics_states.rope_state import RopeState

class Physics(Component):
    def __init__(self):
        super().__init__()

        self.state = AirState(self)
        
        self.stay_on_footholds = False
    
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

    def apply_force(self, force):
        match self.state:
            case AirState():
                self.state.force += force
            case GroundState():
                self.state.force += force.x

    def dislodge(self, keep_vel=True):
        """Detatch from foothold"""
        if not self.on_ground:
            return

        vel = Vector2()
        if keep_vel:
            vel = Vector2(self.state.vel, 0)
        self.state = AirState(self)
        self.state.vel = vel
    
    def grab_rope(self, rope):
        #TODO: move to a rope state
        pos = self.get_component(Position).pos
        pos_on_rope = (pos - rope.top).project(rope.bottom - rope.top)
        rope_pos = project_onto_foothold(pos_on_rope, rope.bottom, rope.top)

    def update(self):
        #TODO: allow transitioning between multiple states per frame?
        self.state.update()
        