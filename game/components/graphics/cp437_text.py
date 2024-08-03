import math

import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from .renderable import Renderable
from game.utils import tint

def text_to_cp437(text):
    coords = []
    for char in text:
        c = ord(char)
        x = c % 16
        y = math.floor(c / 16)
        coords.append(Vector2(x, y))
    
    return coords

class CP437Text(Renderable):
    def __init__(self, text, color=(255, 255, 255), shadow_color=None, shadow_offset=Vector2(1, 1)):
        super().__init__()
        self.image = pygame.image.load("game/assets/images/cp437.png")
        self.text = text
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        
        self.requirements = [Position]

        self.set_color(color)
        self.set_shadow_color(shadow_color)
    
    def set_color(self, color):
        self.primary_image = tint(self.image, color)
    
    def set_shadow_color(self, color):
        self.shadow_color = color

        if color is None:
            return

        self.shadow_image = tint(self.image, color)

    def render(self, screen, camera=None):
        pos = self.get_component(Position).pos
        
        if camera is not None:
            pos = camera.to_screen(pos)

        coords = text_to_cp437(self.text)

        for i, coord in enumerate(coords):
            x = pos.x + i * 8
            y = pos.y
            char_x = coord.x * 8
            char_y = coord.y * 8
            if self.shadow_color is not None:
                screen.blit(self.shadow_image, (x + self.shadow_offset.x, y + self.shadow_offset.y, 8, 8), (char_x, char_y, 8, 8))
            screen.blit(self.primary_image, (x, y, 8, 8), (char_x, char_y, 8, 8))
            