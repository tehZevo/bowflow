import pygame

from .renderable import Renderable
from .position import Position
from ..constants import PPU

class Sprite(Renderable):
    def __init__(self):
        super().__init__()
        self.image = None
    
    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        #TODO: for now, scale to 1 unit
        self.image = pygame.transform.scale(self.image, (PPU, PPU))
    
    def render(self, screen, camera=None):
        if self.image is None:
            return

        pos = self.get_component(Position).pos

        if camera is not None:
            pos = camera.to_screen(pos)
        
        rect = pygame.Rect(pos.x - PPU / 2, pos.y - PPU, 0, 0) #TODO: how to scale images?
        screen.blit(self.image, rect)