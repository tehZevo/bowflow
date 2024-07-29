from pygame.math import Vector2

from .action import Action
from ..components.physics import Physics
from ..components.actor import Actor

class Climb(Action):
    def __init__(self, dir):
        super().__init__()
        self.dir = dir
        self.interruptible = True
    
    def update(self, entity):
        self.done = True
        
        phys = entity.get_component(Physics)
        actor = entity.get_component(Actor)
        
        phys.apply_force(Vector2(0, self.dir / 20))
        