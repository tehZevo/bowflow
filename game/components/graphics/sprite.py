import math

import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from .renderable import Renderable
from game.constants import DT

#TODO: make spritedef with data for each sprite
class Sprite(Renderable):
    def __init__(self, image_path=None, states=1, frames=1, speed=1, offset=None):
        super().__init__()
        self.image = None
        self.speed = 1
        self.time = 0
        self.surfs = None
        self.frame = 0
        self.state = 0

        #determine based on image, states, frames
        self.width = None
        self.height = None

        if image_path is not None:
            self.set_image(image_path, frames, states)

        self.offset = Vector2() if offset is None else offset
        self.requirements = [Position]
        self.flip_x = False
        self.flip_y = False
    
    def set_image(self, image_path, states=1, frames=1):
        """Assumes image is evenly divisible by number of frames (x) and number of states (y)
        Builds a 2d array of subsurfaces from the image"""
        img = pygame.image.load(image_path)
        width = math.floor(img.get_width() / frames)
        height = math.floor(img.get_height() / states)

        self.width = width
        self.height = height
        self.state = 0
        self.frame = 0
        self.time = 0

        self.surfs = []
        for s in range(states):
            surfs = []
            for f in range(frames):
                surf = img.subsurface((f * width, s * height, width, height))
                surfs.append(surf)
            self.surfs.append(surfs)

        self.image = img
    
    def anchor_bottom(self):
        height_units = self.width / PPU
        width_units = self.height / PPU
        self.offset = Vector2(-width_units / 2, -height_units)
    
    def render(self, screen, camera=None):
        if self.image is None:
            return
        
        self.time += DT
        if self.time >= 1 / len(self.surfs[0]):
            self.time = 0
            self.frame += 1
            if self.frame >= len(self.surfs[0]):
                self.frame = 0
        
        surf = self.surfs[self.state][self.frame]

        pos = self.get_component(Position).pos
        offset = self.offset
        
        if camera is not None:
            pos = camera.to_screen(pos)
            offset = self.offset * PPU

        rect = pygame.Rect(pos.x + offset.x, pos.y + offset.y, 0, 0)
        screen.blit(pygame.transform.flip(surf, self.flip_x, self.flip_y), rect)