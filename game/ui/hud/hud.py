import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.core import ObjectID

from pygame_gui.elements import UIStatusBar, UILabel

from .hud_bar import HudBar
from .level_label import LevelLabel
from ...constants import HUD_BAR_LENGTH, HUD_BAR_HEIGHT

#TODO: for all skills that have cooldowns, draw cooldown icon in hud

class Hud:
    def __init__(self):
        self.level_label = LevelLabel(pygame.Rect(0, 0, HUD_BAR_LENGTH, HUD_BAR_HEIGHT * 2), level=1)
        self.hp_bar = HudBar(
            pygame.Rect(HUD_BAR_LENGTH, 0, HUD_BAR_LENGTH, HUD_BAR_HEIGHT),
            max_value=1,
            value=0,
            name="HP",
            class_id="@health_bar",
        )
        self.mp_bar = HudBar(
            pygame.Rect(HUD_BAR_LENGTH * 2, 0, HUD_BAR_LENGTH, HUD_BAR_HEIGHT),
            max_value=1,
            value=0,
            name="MP",
            class_id="@mana_bar",
        )
        self.exp_bar = HudBar(
            pygame.Rect(HUD_BAR_LENGTH, HUD_BAR_HEIGHT, HUD_BAR_LENGTH * 2, HUD_BAR_HEIGHT),
            max_value=1,
            value=0,
            name="EXP",
            class_id="@exp_bar",
            include_percent=True,
        )