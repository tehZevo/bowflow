import math

import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from ..graphics.renderable import Renderable
from game.utils import tint

class UIBar(Renderable):
    def __init__(self, width=8, color=(255, 0, 0), bg_color=(127, 127, 127)):
        super().__init__()
        self.image = pygame.image.load("game/assets/images/bar-8-2.png")
        
        self.width = width
        self.percent = 0
        self.set_color(color)
        self.set_bg_color(bg_color)

        self.requirements = [Position]
    
    def set_color(self, color):
        self.fg_image = tint(self.image, color)
    
    def set_bg_color(self, bg_color):
        self.bg_image = tint(self.image, bg_color)

    def set_percent(self, percent):
        self.percent = percent

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
    
    def anchor_bottom(self):
        height_units = self.image.get_height() / PPU
        width_units = self.image.get_width() / PPU
        self.offset = Vector2(-width_units / 2, -height_units)
    
    def render(self, screen, camera=None):
        pos = self.get_component(Position).pos
        
        for cell in range(self.width):
            #determine row from sprite sheet to render
            row = 0 if cell == 0 else 2 if cell == self.width - 1 else 1
            #determine column to render
            val = math.floor(self.percent * self.width)
            if val > cell:
                col = 8
            elif val < cell:
                col = 0
            else:
                col = math.floor(self.percent * self.width * 9) % 9
            
            screen.blit(self.bg_image, (pos.x + 8 * cell, pos.y + 0, 8, 8), (8 * 8, row * 8, 8, 8))
            screen.blit(self.fg_image, (pos.x + 8 * cell, pos.y + 0, 8, 8), (col * 8, row * 8, 8, 8))