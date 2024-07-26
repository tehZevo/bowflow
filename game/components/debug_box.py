import pygame

from .renderable import Renderable
from ..constants import PPU, DT

class DebugBox(Renderable):
    def __init__(self, min, max, color=(255, 0, 0), alpha=64, time=1):
        super().__init__()
        self.min = min
        self.max = max
        self.color = color
        self.alpha = alpha
        self.time = time
    
    def update(self):
        self.time -= DT
        if self.time <= 0:
            self.entity.remove()
            
    def render(self, screen, camera=None):
        #TODO: check that this drawing is correct
        min = camera.to_screen(self.min)
        max = camera.to_screen(self.max)

        #TODO: make to_screen_rect or something to do this for me
        y = min.y
        min.y = max.y
        max.y = y
        
        s = pygame.Surface((max.x - min.x, max.y - min.y))
        s.set_alpha(self.alpha)
        s.fill(self.color)
        screen.blit(s, min)