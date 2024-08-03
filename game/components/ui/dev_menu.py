import math

import pygame
from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from game.components.ui.menu import Menu
from game.components.game_master import GameMaster
from game.components.actor.player import Player
from game.components.ui.menu_items.lambda_item import LambdaItem
from game.components.ui.menu_items.close_item import CloseItem

class DevMenu(Menu):
    def __init__(self):
        super().__init__([
            LambdaItem("Exp me!", self.give_player_exp),
            CloseItem(),
        ], cancelable=True)
    
    def give_player_exp(self, menu):
        #TODO: improve experience of getting player
        player = menu.world.get_all_components(GameMaster)[0].game.world.get_all_components(Player)[0]
        player.give_exp(100)