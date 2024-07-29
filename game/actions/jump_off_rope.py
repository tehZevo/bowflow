from pygame.math import Vector2

from .action import Action
from game.components.physics.physics import Physics

class JumpOffRope(Action):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
    
    def start(self, entity):
        self.done = True

        phys = entity.get_component(Physics)
        if not phys.on_rope:
            return

        phys.drop_from_rope(self.direction)
        