import math

import pygame
from pygame.math import Vector2

from game.constants import PPU
from ..physics.position import Position
from .renderable import Renderable
from game.constants import DT

class Sprite(Renderable):
    def __init__(self, spritedef=None):
        super().__init__()
        self.surfs = {}
        
        if spritedef is not None:
            self.set_spritedef(spritedef)

        self.offset = Vector2()
        self.requirements = [Position]
        self.flip_x = False
        self.flip_y = False
    
    def set_spritedef(self, spritedef):
        self.spritedef = spritedef
        self.time = 0
        self.frame = 0
        self.state = "idle" #TODO: default state in spritedef?
        self.surfs = self.spritedef.load_surfs()
        #TODO: each state should have its own width/height
        self.width = self.surfs[self.state][0].get_width()
        self.height = self.surfs[self.state][0].get_height()

    #TODO: move offset to sprite def/states
    def anchor_bottom(self):
        height_units = self.width / PPU
        width_units = self.height / PPU
        self.offset = Vector2(-width_units / 2, -height_units)
    
    def render(self, screen, camera=None):
        if self.spritedef is None:
            return
        
        self.time += DT
        if self.time >= 1 / len(self.surfs[self.state]) / self.spritedef.speed:
            self.time = 0
            self.frame += 1
            if self.frame >= len(self.surfs[self.state]):
                self.frame = 0
        
        surf = self.surfs[self.state][self.frame]

        pos = self.get_component(Position).pos
        offset = self.offset
        
        if camera is not None:
            pos = camera.to_screen(pos)
            offset = self.offset * PPU

        rect = pygame.Rect(pos.x + offset.x, pos.y + offset.y, 0, 0)
        screen.blit(pygame.transform.flip(surf, self.flip_x, self.flip_y), rect)