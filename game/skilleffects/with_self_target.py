from .skilleffect import SkillEffect
from game.components.skill import Skill

class WithSelfTarget(SkillEffect):
    def __init__(self, apply=[]):
        super().__init__()
        self.effect_generators = apply
    
    def start(self, skill):
        #TODO: dedupe with for_each_target
        target = skill.caster
        for gen in self.effect_generators:
            skill_comp = Skill(gen())
            skill_comp.caster = skill.caster
            skill_comp.target = target
            skill.world.create_entity([skill_comp])
            skill_comp.start()