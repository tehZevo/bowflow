from pygame.math import Vector2

from game.ecs import Component
from .sprite import Sprite

from game.constants import DT, PPU

class Effect(Component):
    def __init__(self, effect_path=None, time=1):
        super().__init__()
        self.time = time
        self.effect_path = effect_path
    
    def init(self):
        #TODO: reconsider how offsets are managed for sprites.. this is getting messy
        sprite = self.get_component(Sprite)
        sprite.set_image(self.effect_path)

        offset = Vector2(-sprite.image.get_width() / PPU / 2, -sprite.image.get_height() / PPU / 2)
        sprite.offset = offset

    def update(self):
        self.time -= DT
        if self.time <= 0:
            self.entity.remove()