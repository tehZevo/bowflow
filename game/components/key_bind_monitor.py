import pygame
from pygame.math import Vector2

from game.ecs import Component
from .key_bind_listener import KeyBindListener

def pressed_binds(bind_map):
    pressed = pygame.key.get_pressed()
    binds = [bind for key, bind in bind_map.items() if pressed[key]]
    return binds

#TODO: update bindings if they change...
#TODO: or do we want to elevate this functionality all the way up to main?

class KeyBindMonitor(Component):
    """Monitors pygame key presses based on bindings in player data"""
    def __init__(self, player_data):
        super().__init__()
        self.player_data = player_data
    
    def get_pressed_binds(self):
        actions = pressed_binds(self.player_data.action_binds)
        skills = pressed_binds(self.player_data.skill_binds)
        return actions, skills

    def update(self):
        actions, skills = self.get_pressed_binds()
        
        for listener in self.entity.get_all_components(KeyBindListener):
            listener.on_key_binds(actions, skills)
        