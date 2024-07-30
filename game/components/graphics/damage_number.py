import pygame
from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from ..graphics.renderable import Renderable

from game.constants import DT, PPU

SEPARATION = 32

class DamageNumber(Renderable):
    def __init__(self, number, time=1):
        super().__init__()
        self.time = time
        self.elapsed_time = 0
        self.number = str(int(number))
        self.images = []
        self.requirements = [Position]
    
    def init(self):
        #TODO: handle k/m/b/t
        self.images = [pygame.image.load(f"game/assets/images/numbers/{n}.png") for n in self.number]

    def update(self):
        self.elapsed_time += DT
        if self.elapsed_time >= self.time:
            self.entity.remove()
        
        pos = self.get_component(Position)
        pos.set_pos(pos.pos + Vector2(0, DT / 2))
        
    
    def render(self, screen, camera):
        pos = self.get_component(Position).pos

        if camera is not None:
            pos = camera.to_screen(pos)

        for x, image in enumerate(self.images):
            rect = pygame.Rect(pos.x + x * SEPARATION - len(self.images) / 2 * SEPARATION, pos.y, 0, 0)
            screen.blit(image, rect)
