import random

from game.ecs import Component
from game.data.exp_calcs import calc_mob_exp
from game.components.actor.monster import Monster
from game.components.physics.physics import Physics
from game.components.physics.position import Position
from game.components.graphics.sprite import Sprite
from game.components.actor.actor import Actor
from game.components.physics.foothold import Foothold

from game.constants import DT

class Spawner(Component):
    #TODO: provide mobdef
    def __init__(self, per_wave=4, wave_time=5, spawn_max=10):
        super().__init__()
        self.per_wave = per_wave
        self.wave_time = wave_time
        self.spawn_max = spawn_max

        self.remaining_spawn_time = self.wave_time

        self.mobs = []
    
    def spawn(self):
        fh = self.get_component(Foothold)
        rand_t = random.random()
        
        monster = self.world.create_entity([
            Position(),
            Physics(),
            Sprite(),
            Actor(),
            Monster(),
        ])

        monster.get_component(Physics).move_to_foothold(fh, rand_t)

        self.mobs.append(monster)

    def spawn_wave(self):
        for _ in range(self.per_wave):
            if len(self.mobs) >= self.spawn_max:
                break
            self.spawn()

    def update(self):
        self.remaining_spawn_time -= DT
        if self.remaining_spawn_time <= 0:
            self.spawn_wave()
            self.remaining_spawn_time = self.wave_time
        
        self.mobs = [m for m in self.mobs if m.alive]
        
        #TODO: remove dead mobs
            