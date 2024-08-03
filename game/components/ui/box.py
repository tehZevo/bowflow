import math

import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from game.components.graphics.renderable import Renderable
from game.utils import tint

def sprite_coord(x, y, width, height):
    if x == 0 and y == 0: return Vector2(0, 0)
    if x == width - 1 and y == 0: return Vector2(2, 0)
    if x == 0 and y == height - 1: return Vector2(0, 2)
    if x == width - 1 and y == height - 1: return Vector2(2, 2)
    if x == 0: return Vector2(0, 1)
    if x == width - 1: return Vector2(2, 1)
    if y == 0: return Vector2(1, 0)
    if y == height - 1: return Vector2(1, 2)
    return Vector2(1, 1)

class Box(Renderable):
    def __init__(self, pos=None, size=None):
        super().__init__()
        self.pos = Vector2(0, 0) if pos is None else pos
        self.size = Vector2(32, 6) if size is None else size
        self.image = pygame.image.load("game/assets/images/textbox.png")
        
        self.requirements = [Position]

    def render(self, screen, camera=None):
        pos = self.get_component(Position).pos
        
        for y in range(int(self.size.y)):
            for x in range(int(self.size.x)):
                coord = sprite_coord(x, y, self.size.x, self.size.y)
                screen.blit(self.image, (x * 8, y * 8, 8, 8), (coord.x * 8, coord.y * 8, 8, 8))
