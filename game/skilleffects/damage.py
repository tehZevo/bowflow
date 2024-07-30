import random

from .skilleffect import SkillEffect
from ..components.actor import Actor

class Damage(SkillEffect):
    def __init__(self, power):
        super().__init__()
        self.power = power
    
    def start(self, skill):
        skill.done = True
        
        actor = skill.target.get_component(Actor)

        #TODO: calculate real damage range
        actor.damage(self.power * (1 + random.random() * 0.2 - 0.1), skill.caster)
