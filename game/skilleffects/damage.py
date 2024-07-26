from .skilleffect import SkillEffect
from ..components.actor import Actor

class Damage(SkillEffect):
    def __init__(self, power):
        super().__init__()
        self.power = power
    
    def start(self, skill):
        actor = skill.target.get_component(Actor)

        actor.damage(self.power, skill.caster)

        skill.done = True