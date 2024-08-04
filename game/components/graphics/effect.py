from pygame.math import Vector2

from game.ecs import Component
#TODO: for now, use image, but eventually, effects will be sprites (because animation)
from .image import Image

from game.constants import DT, PPU

class Effect(Component):
    def __init__(self, effect_path=None, time=1):
        super().__init__()
        self.time = time
        self.effect_path = effect_path
        self.requirements = [Image]
    
    def init(self):
        #TODO: reconsider how offsets are managed for sprites.. this is getting messy
        image = self.get_component(Image)
        image.set_image(self.effect_path)

        #TODO: make image/sprite .anchor_center
        offset = Vector2(-image.image.get_width() / PPU / 2, -image.image.get_height() / PPU / 2)
        image.offset = offset

    def update(self):
        self.time -= DT
        if self.time <= 0:
            self.entity.remove()