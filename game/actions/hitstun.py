from pygame.math import Vector2

from .action import Action
from ..components.physics.physics import Physics
from ..components.physics.position import Position
from ..components.actor import Actor

from game.constants import HITSTUN_TIME, HITSTUN_DISTANCE, DT

class Hitstun(Action):
    def __init__(self, dir):
        super().__init__()
        self.dir = dir
        self.time = HITSTUN_TIME
        self.start_x = None
        self.target_x = None
    
    def start(self, entity):
        phys = entity.get_component(Physics)
        position = entity.get_component(Position)
        
        if not phys.on_ground:
            self.done = True
            return

        self.start_x = position.pos.x
        self.target_x = self.start_x + HITSTUN_DISTANCE * self.dir

    def update(self, entity):
        self.time -= DT

        if self.time <= 0:
            self.done = True
            return
        
        phys = entity.get_component(Physics)
        position = entity.get_component(Position)
        actor = entity.get_component(Actor)

        x = self.target_x + (position.pos.x - self.target_x) * self.time / HITSTUN_TIME
        force = x - position.pos.x - phys.state.vel / 1
        
        phys.apply_force(Vector2(force / 10, 0))
        