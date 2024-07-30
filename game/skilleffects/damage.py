import random

from pygame.math import Vector2

from .skilleffect import SkillEffect
from ..components.actor.actor import Actor
from ..components.physics.position import Position
from ..components.graphics.damage_number import DamageNumber

class Damage(SkillEffect):
    #TODO: custom delay for each hit
    def __init__(self, power, hits=1):
        super().__init__()
        self.power = power
        self.hits = hits
    
    def start(self, skill):
        skill.done = True
        
        actor = skill.target.get_component(Actor)

        #TODO: real damage calcs
        damage = 0
        for i in range(self.hits):
            damage += self.power * (1 + random.random() * 0.2 - 0.1)

            skill.world.create_entity([
                Position(skill.target.get_component(Position).pos + Vector2(0, 2)),
                DamageNumber(damage, stack=i, delay=i * 0.25),
            ])

        actor.damage(damage, skill.caster)
