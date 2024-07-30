import pygame
from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from ..graphics.renderable import Renderable

from game.constants import DT, PPU

SEPARATION = 24
STACK_SEPARATION = 48
DAMAGE_NUMBER_TIME = 3
DAMAGE_NUMBER_HEIGHT = 1

class DamageNumber(Renderable):
    def __init__(self, number, stack=0, delay=0):
        super().__init__()
        self.number = str(int(number))
        self.delay = delay
        self.stack = stack
        self.time = 0
        
        self.images = []
        self.requirements = [Position]
        self.sound_played = False
        self.start_pos = None
    
    def init(self):
        #TODO: handle k/m/b/t
        self.images = [pygame.image.load(f"game/assets/images/numbers/{n}.png") for n in self.number]

        self.hit_sound = pygame.mixer.Sound("game/assets/audio/hit.wav") #TODO: store this somewhere

        self.start_pos = self.get_component(Position).pos

    def update(self):
        #updadte delay
        self.delay -= DT
        if self.delay > 0:
            return

        self.time += DT
        
        #play sound
        if not self.sound_played:
            pygame.mixer.Sound.play(self.hit_sound)
            self.sound_played = True

        #update position
        pos = self.get_component(Position)
        pos.set_pos(self.start_pos + Vector2(0, self.time / DAMAGE_NUMBER_TIME * DAMAGE_NUMBER_HEIGHT))

        #TODO: fade out for last N seconds
        if self.time >= DAMAGE_NUMBER_TIME:
            self.entity.remove()
        
    def render(self, screen, camera):
        if self.delay >= 0:
            return
            
        pos = self.get_component(Position).pos

        if camera is not None:
            pos = camera.to_screen(pos)

        for x, image in enumerate(self.images):
            rect = pygame.Rect(
                pos.x + x * SEPARATION - len(self.images) / 2 * SEPARATION,
                pos.y - self.stack * STACK_SEPARATION,
                0, 0
            )
            screen.blit(image, rect)
