import pygame
from pygame.math import Vector2

from ..graphics import Renderable

class Foothold(Renderable):
    def __init__(self, start, end, prev=None, next=None, allow_jump_down=True):
        super().__init__()

        self.start = start
        self.end = end
        self.prev = prev
        self.next = next
        #TODO: use this in physics
        self.allow_jump_down = allow_jump_down
    
    def calc_position(self, foothold_pos):
        return self.start + (self.end - self.start) * foothold_pos

    def render(self, screen, camera=None):
        if camera is None:
            return
        
        start = camera.to_screen(self.start)
        end = camera.to_screen(self.end)
        pygame.draw.line(screen, (0, 0, 255), start, end, width=1)
        pygame.draw.circle(screen, (0, 0, 255), start, 3, width=1 if self.prev is None else 0)
        pygame.draw.circle(screen, (0, 0, 255), end, 3, width=1 if self.next is None else 0)