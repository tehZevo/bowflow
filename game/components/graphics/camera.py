from pygame.math import Vector2

from game.ecs import Component
from game.constants import PPU, WIDTH_UNITS, HEIGHT_UNITS
from ..physics.position import Position
from game.utils import closest_point_in_box

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
        self.offset = Vector2(0, 2)
        self.box = Vector2(2, 2)
    
    def set_target(self, entity):
        self.target = target

    def to_screen(self, pos):
        """scale and apply camera offset to given position; also handles flipping y for you"""
        
        pos = (pos - self.offset) * PPU
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
        pos_comp = self.get_component(Position)
        camera_pos = pos_comp.pos

        target_pos = closest_point_in_box(camera_pos, target_pos, self.box)


        pos_comp.set_pos(camera_pos + (target_pos - camera_pos) * self.speed)

