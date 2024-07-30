from .skilleffect import SkillEffect
from game.components.skill import Skill

class WithSelfTarget(SkillEffect):
    def __init__(self, apply=[]):
        super().__init__()
        self.effect_generators = apply
        self.effects = []
    
    def start(self, skill):
        #TODO: dedupe with for_each_target
        target = skill.caster
        for gen in self.effect_generators:
            skill_comp = Skill(gen())
            skill_comp.caster = skill.caster
            skill_comp.target = target
            effect = skill.world.create_entity([skill_comp])
            skill_comp.start()
            self.effects.append(effect)
    
    def update(self, skill):
        #target effects are not complete until all of their children are complete
        if len(self.effects) == 0 or all([effect.get_component(Skill).done for effect in self.effects]):
            skill.done = True