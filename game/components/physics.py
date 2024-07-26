from pygame.math import Vector2

from ..ecs.component import Component
from .position import Position
from .foothold import Foothold
from ..utils import intersect, project_onto_foothold
from ..constants import GRAVITY, GROUND_FRICTION, AIR_FRICTION

class Physics(Component):
    def __init__(self):
        super().__init__()

        self.vel = Vector2()
        self.force = Vector2()

        self.on_ground = False
        self.foothold = None
        self.foothold_pos = None #TODO: make function for dislodging from foothold
    
    def apply_force(self, force):
        self.force = self.force + force

    def air_update(self):
        pos = self.get_component(Position)
        self.apply_force(Vector2(0, GRAVITY))

        #TODO: mass?
        self.vel = self.vel + self.force
        #TODO: air friction?

        self.force = Vector2()

        footholds = self.world.get_all_components(Foothold)

        if self.vel.y <= 0:
            #TODO: find first collision in direction instead of first based on iteration order
            for fh in footholds:
                #TODO: multiply vel by fixed DT offset? right now its per-frame movement
                intersection_pos = intersect(fh.start, fh.end, pos.pos, pos.pos + self.vel)
                if intersection_pos is not None:
                    fh_t = project_onto_foothold(intersection_pos, fh.start, fh.end)
                    fh_pos = fh.start + (fh.end - fh.start) * fh_t

                    self.on_ground = True
                    self.foothold = fh
                    self.foothold_pos = fh_t
                    pos.set_pos(fh_pos)

        pos.set_pos(pos.pos + self.vel)

    def dislodge(self):
        self.on_ground = False
        self.foothold = None
        self.foothold_pos = 0

    def ground_update(self):
        pos = self.get_component(Position)

        #TODO: if force is large enough, dislodge from ground?

        self.vel = self.vel + self.force
        self.vel.y = 0
        self.force = Vector2()
        
        fh_width = self.foothold.end.x - self.foothold.start.x
        fh_speed = (self.foothold.end - self.foothold.start).length() / fh_width #TODO: beware div by 0 with vertical footholds

        self.foothold_pos = self.foothold_pos + self.vel.x / fh_width * fh_speed

        fh_pos = self.foothold.start + (self.foothold.end - self.foothold.start) * self.foothold_pos
        pos.set_pos(fh_pos)

        self.vel = self.vel * (1 - GROUND_FRICTION)

        #TODO: move to prev/next foothold if any, else dislodge
        if self.foothold_pos < 0 or self.foothold_pos > 1:
            self.dislodge()
            return

    def update(self):
        if not self.on_ground:
            self.air_update()
        
        #TODO: should i elif this?
        if self.on_ground:
            self.ground_update()
            
        