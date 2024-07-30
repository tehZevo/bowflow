from .physics_state import PhysicsState

from pygame.math import Vector2

from game.ecs import Component
from game.utils import intersect, project_onto_foothold
from game.constants import GROUND_FRICTION
from ..position import Position
from ..foothold import Foothold
from ..wall import Wall

class GroundState(PhysicsState):
    def __init__(self, physics):
        super().__init__(physics)
        self.vel = 0
        self.force = 0

        self.foothold = None
        self.foothold_pos = None
    
    def update_pos(self):
        pos = self.foothold.start + (self.foothold.end - self.foothold.start) * self.foothold_pos
        self.physics.get_component(Position).set_pos(pos)

    def move_relative(self, amount, stay_on_footholds=True):
        """Move relative to current foothold, taking in neighboring footholds into account"""
        fh_width = self.foothold.end.x - self.foothold.start.x
        fh_speed = (self.foothold.end - self.foothold.start).length() / fh_width #TODO: beware div by 0 with vertical footholds
        
        self.foothold_pos = self.foothold_pos + amount / fh_width * fh_speed

        if stay_on_footholds:
            self.foothold_pos = max(0, min(1, self.foothold_pos))
            
        if self.foothold_pos < 0 or self.foothold_pos > 1:
            if self.foothold_pos < 0 and self.foothold.prev is not None:
                self.foothold = self.foothold.prev
                self.foothold_pos = 1 + self.foothold_pos
            elif self.foothold_pos > 1 and self.foothold.next is not None:
                self.foothold = self.foothold.next
                self.foothold_pos = 1 - self.foothold_pos
            else:
                self.physics.dislodge()

    def update(self):
        pos = self.physics.get_component(Position)

        #TODO: if force is large enough, dislodge from ground?
        #TODO: when falling onto FH, project vel onto FH so you "slide down" as you land

        self.vel = self.vel + self.force
        self.force = 0

        #TODO: beware, this isnt exactly correct since FH uses vel to mean left/right walking speed
        for wall in self.physics.world.get_all_components(Wall):
            intersection_pos = intersect(wall.start, wall.end, pos.pos, pos.pos + Vector2(self.vel, 0))
            if intersection_pos is None:
                continue
            
            #TODO: do we need to modify velocity's length?
            #TODO: maybe we need to keep a "delta_pos" vector and manipulate that through wall and fh logic
            if wall.direction == 0 \
                or (wall.direction == 1 and self.vel <= 0) \
                or (wall.direction == -1 and self.vel >= 0):
                #instead of projecting, just stop for now..
                # we would need extra logic for if an angled wall "lifts" the player off a FH..
                self.vel = 0
                #TODO: set fh position to wall position
        
        self.move_relative(self.vel, stay_on_footholds=self.physics.stay_on_footholds)
        self.update_pos()
        self.vel = self.vel * (1 - GROUND_FRICTION)