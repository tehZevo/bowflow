import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from .renderable import Renderable

class Sprite(Renderable):
    def __init__(self, image_path=None, offset=None):
        super().__init__()
        self.image = None

        if image_path is not None:
            self.set_image(image_path)

        self.offset = Vector2() if offset is None else offset
        self.requirements = [Position]
    
    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        # self.image = pygame.transform.scale(self.image, (PPU, PPU))
    
    def render(self, screen, camera=None):
        if self.image is None:
            return

        pos = self.get_component(Position).pos
        offset = self.offset
        
        if camera is not None:
            pos = camera.to_screen(pos)
            offset = self.offset * PPU

        rect = pygame.Rect(pos.x + offset.x, pos.y + offset.y, 0, 0)
        screen.blit(self.image, rect)