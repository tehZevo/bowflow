import pygame
from pygame.math import Vector2

from ..graphics import Renderable

class Rope(Renderable):
    def __init__(self, top, length):
        super().__init__()

        self.top = top
        self.length = length
        self.bottom = self.top - Vector2(0, self.length)

    def render(self, screen, camera=None):
        if camera is None:
            return
        
        top = camera.to_screen(self.top)
        bottom = camera.to_screen(self.bottom)
        pygame.draw.line(screen, (0, 128, 0), top, bottom)
        pygame.draw.circle(screen, (0, 128, 0), top, 8, width=0)