import math

import pygame
from pygame.math import Vector2

from game.ecs import Component
from game.constants import PPU
from ..physics.position import Position
from game.components.ui.ui_bar import UIBar

HP_BAR_COLOR = (255, 0, 0)
MP_BAR_COLOR = (0, 0, 255)
EXP_BAR_COLOR = (255, 255, 0)
BAR_BG_COLOR = (127, 127, 127)

class HUD(Component):
    def __init__(self, width=8, color=(255, 0, 0), bg_color=(127, 127, 127)):
        super().__init__()
        
        self.hp_bar = None
        self.mp_bar = None
        self.exp_bar = None
    
    def init(self):
        self.hp_bar = UIBar(width=8, color=HP_BAR_COLOR, bg_color=BAR_BG_COLOR)
        self.world.create_entity([
            Position(Vector2(0, 0)),
            self.hp_bar,
        ])

        self.mp_bar = UIBar(width=8, color=MP_BAR_COLOR, bg_color=BAR_BG_COLOR)
        self.world.create_entity([
            Position(Vector2(8 * 8, 0)),
            self.mp_bar,
        ])

        self.exp_bar = UIBar(width=16, color=EXP_BAR_COLOR, bg_color=BAR_BG_COLOR)
        self.world.create_entity([
            Position(Vector2(0, 8)),
            self.exp_bar,
        ])