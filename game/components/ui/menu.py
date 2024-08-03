import math

import pygame
from pygame.math import Vector2

from game.ecs import Component
from game.constants import PPU
from ..physics.position import Position
from game.components.ui.ui_bar import UIBar
from game.components.ui.text import Text
from game.components.ui.box import Box
from game.components.game_master import GameMaster
from game.components.key_bind_listener import KeyBindListener

class Menu(Component, KeyBindListener):
    def __init__(self, items=[], cancelable=True):
        super().__init__()
        self.items = items
        self.box = None
        self.cursor_pos = 0
        self.ents = []
        self.item_texts = []
        self.cancelable = cancelable
    
    def init(self):
        pass
    
    def on_key_binds(self, binds):
        if "move_down" in binds.pressed_actions:
            self.move_cursor(1)
        if "move_up" in binds.pressed_actions:
            self.move_cursor(-1)
        if "select" in binds.pressed_actions:
            self.select()
        if "back" in binds.pressed_actions and self.cancelable:
            self.close()
        
    def update_texts(self):
        for i, (item, item_text) in enumerate(zip(self.items, self.item_texts)):
            if i == self.cursor_pos:
                item_text.text = f">{item.text}"
            else:
                item_text.text = f" {item.text}"

    def move_cursor(self, dir):
        self.cursor_pos += dir
        self.cursor_pos = max(0, min(self.cursor_pos, len(self.items) - 1))
        self.update_texts()

    def select(self):
        self.items[self.cursor_pos].select(self)

    def cancel(self):
        #TODO
        pass
    
    def create(self):
        #TODO: intercept input
        game = self.world.get_all_components(GameMaster)[0].game
        game.paused = True

        box = self.world.create_entity([
            Box(Vector2(0, 0), Vector2(10, 16)),
        ])
        self.ents.append(box)

        for i, item in enumerate(self.items):
            text = Text(f" {item.text}")
            self.item_texts.append(text)
            #TODO: offset by our position
            pos = Vector2(8, (i + 1) * 8)
            ent = self.world.create_entity([Position(pos), text])
            self.ents.append(ent)
        
        self.update_texts()

    def close(self):
        #TODO hmm...
        from game.components.ui.ui_manager import UIManager
        self.world.get_all_components(UIManager)[0].close_menu()
        
    def destroy(self):
        #TODO: remove all our ents and self
        for ent in self.ents:
            ent.remove()
        
        self.entity.remove()