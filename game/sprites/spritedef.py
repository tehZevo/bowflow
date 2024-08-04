import math

import pygame

#TODO: add default speed to returned structure?
# this may require a new type SpriteState that has surfs, speed, (palettes?) etc.
# alternatively, the spritedef will just load and cache its surfs and also store extra metadata

#TODO: per-state speed
class SpriteDef:
    def __init__(self, states={}, speed=1):
        """States = a dictionary of (path, num_frames) tuples"""
        self.states = states
        self.speed = speed
    
    def load_state_surfs(self, path, frames):
        img = pygame.image.load(path)
        width = math.floor(img.get_width() / frames)
        height = img.get_height()
        
        surfs = []
        for f in range(frames):
            surf = img.subsurface((f * width, 0, width, height))
            surfs.append(surf)
        
        return surfs
        
    def load_surfs(self):
        """Returns a dictionary of state name -> list of surfs"""
        return {name: self.load_state_surfs(path, frames) for name, (path, frames) in self.states.items()}