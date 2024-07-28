import pygame
from pygame.math import Vector2

from ..graphics import Renderable

class Wall(Renderable):
    def __init__(self, start, end, direction=0):
        """direction is the facing direction of the wall (1=right, -1=left), if 0, wall operates both ways"""
        super().__init__()

        self.start = start
        self.end = end
        self.direction = direction

    def render(self, screen, camera=None):
        if camera is None:
            return
        
        start = camera.to_screen(self.start)
        end = camera.to_screen(self.end)
        pygame.draw.line(screen, (255, 0, 0), start, end)
        pygame.draw.circle(screen, (255, 0, 0), start, 8, width=0)
        pygame.draw.circle(screen, (255, 0, 0), end, 8, width=0)

        #TODO: draw direction indicator