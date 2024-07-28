import pygame
from pygame.math import Vector2

from ..graphics import Renderable

class Foothold(Renderable):
    def __init__(self, start, end, prev=None, next=None):
        super().__init__()

        self.start = start
        self.end = end
        self.prev = prev
        self.next = next
    
    def calc_position(self, foothold_pos):
        return self.start + (self.end - self.start) * foothold_pos

    def render(self, screen, camera=None):
        if camera is None:
            return
        
        start = camera.to_screen(self.start)
        end = camera.to_screen(self.end)
        pygame.draw.line(screen, (255, 0, 0), start, end)
        pygame.draw.circle(screen, (255, 0, 0), start, 3, width=0)
        pygame.draw.circle(screen, (255, 0, 0), end, 3, width=0)