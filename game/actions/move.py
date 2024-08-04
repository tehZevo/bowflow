from pygame.math import Vector2

from .action import Action
from ..components.physics import Physics
from ..components.actor import Actor
from ..components.graphics.sprite import Sprite

class Move(Action):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.interruptible = True
        
    def start(self, entity):
        sprite = entity.get_component(Sprite)

        #TODO: air/ground check to set sprite state
        sprite.set_state("walk")

    def update(self, entity):
        self.done = True
        
        phys = entity.get_component(Physics)
        actor = entity.get_component(Actor)
        
        phys.apply_force(Vector2(self.speed, 0))
        if self.speed > 0:
            actor.facing_dir = 1
        elif self.speed < 0:
            actor.facing_dir = -1
