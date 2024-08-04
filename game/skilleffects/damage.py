import random
from itertools import accumulate

from pygame.math import Vector2

from .skilleffect import SkillEffect
from ..components.actor.actor import Actor
from ..components.physics.position import Position
from ..components.graphics.damage_number import DamageNumber

DEFAULT_DELAY = 0.25

class Damage(SkillEffect):
    #TODO: custom delay for each hit
    def __init__(self, power, hits=1, delays=None):
        super().__init__()
        self.power = power
        self.hits = hits
        self.delays = [DEFAULT_DELAY for _ in range(hits)] if delays is None else delays
        self.delays = accumulate(self.delays)
    
    def start(self, skill):
        skill.done = True
        
        actor = skill.target.get_component(Actor)

        #TODO: real damage calcs
        damage = 0
        for i, delay in enumerate(self.delays):
            damage_line = self.power * (1 + random.random() * 0.2 - 0.1)
            
            damage += damage_line
            skill.world.create_entity([
                Position(skill.target.get_component(Position).pos + Vector2(0, 2)),
                DamageNumber(damage_line, stack=i, delay=delay),
            ])

        actor.damage(damage, skill.caster)
