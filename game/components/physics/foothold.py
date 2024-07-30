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
        #TODO: parameter for allowing jump down or not
    
    def calc_position(self, foothold_pos):
        return self.start + (self.end - self.start) * foothold_pos

    def render(self, screen, camera=None):
        if camera is None:
            return
        
        start = camera.to_screen(self.start)
        end = camera.to_screen(self.end)
        #TODO: if has prev/next, fill in circle, else leave empty
        pygame.draw.line(screen, (0, 0, 255), start, end, width=3)
        pygame.draw.circle(screen, (0, 0, 255), start, 8, width=3 if self.prev is None else 0)
        pygame.draw.circle(screen, (0, 0, 255), end, 8, width=3 if self.next is None else 0)