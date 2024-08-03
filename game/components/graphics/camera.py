from pygame.math import Vector2

from game.ecs import Component
from game.constants import PPU, WIDTH_UNITS, HEIGHT_UNITS
from ..physics.position import Position

SCREEN_WIDTH = WIDTH_UNITS * PPU
SCREEN_HEIGHT = HEIGHT_UNITS * PPU

class Camera(Component):
    def __init__(self, target=None, speed=0.1):
        super().__init__()

        #TODO: camera box (dont move if target is within a box around camera)
        #TODO: offset camera y (raise above player.. maybe instead of setting a camera target, we update the camera's target position every step?)
        self.target = target
        self.speed = speed
        self.requirements = [Position]
    
    def set_target(self, entity):
        self.target = target

    def to_screen(self, pos):
        """scale and apply camera offset to given position; also handles flipping y for you"""
        
        pos = pos * PPU
        pos = pos - self.get_component(Position).pos * PPU
        pos = pos.elementwise() * Vector2(1, -1)
        pos = pos + Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        return pos

    def update(self):
        if self.target is None:
            return
        
        target_pos = self.target.get_component(Position)
        if target_pos is None:
            return
        
        target_pos = target_pos.pos

        pos = self.get_component(Position)

        pos.set_pos(pos.pos + (target_pos - pos.pos) * self.speed)