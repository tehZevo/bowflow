from .skilleffect import SkillEffect
from game.components.skill import Skill

from ..constants import DEBUG_TARGETS

class ForEachTarget(SkillEffect):
    def __init__(self, in_a, apply=[]):
        super().__init__()
        self.method = in_a
        self.effect_generators = apply
    
    def start(self, skill):
        if DEBUG_TARGETS:
            self.method.debug(skill.caster)
            
        targets = self.method.get_targets(skill.caster)

        for target in targets:
            for gen in self.effect_generators:
                skill_comp = Skill(gen())
                skill_comp.caster = skill.caster
                skill_comp.target = target
                skill.world.create_entity([skill_comp])
                skill_comp.start()