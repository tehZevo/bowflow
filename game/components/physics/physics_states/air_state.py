from pygame.math import Vector2

from .physics_state import PhysicsState
from game.utils import intersect, project_onto_foothold
from game.constants import GRAVITY, AIR_FRICTION
from ..position import Position
from ..foothold import Foothold
from ..wall import Wall

class AirState(PhysicsState):
    def __init__(self, physics):
        super().__init__(physics)
        self.vel = Vector2()
        self.force = Vector2()

        #TODO: add an "ignored footholds" field for down jump
    
    def update(self):
        pos = self.physics.get_component(Position)
        self.physics.apply_force(Vector2(0, GRAVITY))

        #TODO: mass?
        self.vel = self.vel + self.force

        self.force = Vector2()

        for wall in self.physics.world.get_all_components(Wall):
            intersection_pos = intersect(wall.start, wall.end, pos.pos, pos.pos + self.vel)
            if intersection_pos is None:
                continue
            
            #TODO: do we need to modify velocity's length?
            #TODO: maybe we need to keep a "delta_pos" vector and manipulate that through wall and fh logic
            if wall.direction == 0 \
                or (wall.direction == 1 and self.vel.x <= 0) \
                or (wall.direction == -1 and self.vel.x >= 0):
                wall_dir = (wall.end - wall.start).normalize()
                #project vel onto wall
                vel_projected = self.vel.project(wall_dir)
                self.vel = vel_projected
                #TODO: yeah need to subtract vel since we already moved some
                pos.set_pos(intersection_pos)

        footholds = self.physics.world.get_all_components(Foothold)

        if self.vel.y <= 0:
            #TODO: find first collision in direction instead of first based on iteration order
            for fh in footholds:
                #TODO: multiply vel by fixed DT offset? right now its per-frame movement
                intersection_pos = intersect(fh.start, fh.end, pos.pos, pos.pos + self.vel)
                if intersection_pos is None:
                    continue
                
                fh_t = project_onto_foothold(intersection_pos, fh.start, fh.end)
                fh_pos = fh.start + (fh.end - fh.start) * fh_t
                
                #enter grounded state
                self.physics.move_to_foothold(fh, fh_t)
                #TODO: this info wont be included in state update...
                self.physics.state.vel = self.vel.x
        
        pos.set_pos(pos.pos + self.vel)
        self.vel = self.vel * (1 - AIR_FRICTION)