import math

import pygame
from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from game.components.ui.menu import Menu
from game.components.game_master import GameMaster
from game.components.actor.player import Player
from game.components.ui.menu_items.close_item import CloseItem
from game.components.ui.menu_items.open_menu import OpenMenu
from game.components.ui.dev_menu import DevMenu
from game.components.ui.skill_menu import SkillMenu

class MainMenu(Menu):
    def __init__(self, skill_tree):
        super().__init__([
            OpenMenu("Dev", lambda menu: DevMenu()),
            OpenMenu("Skills", lambda menu: SkillMenu(skill_tree)),
            CloseItem(),
        ], cancelable=True)
    
    def give_player_exp(self, menu):
        #TODO: improve experience of getting player
        player = menu.world.get_all_components(GameMaster)[0].game.world.get_all_components(Player)[0]
        player.give_exp(100)