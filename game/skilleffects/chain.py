from .skilleffect import SkillEffect
from game.components.skill import Skill

class Chain(SkillEffect):
    def __init__(self, effects=[]):
        super().__init__()
        self.effects = effects
        self.step = 0
        self.effect = None
    
    def run_next_effect(self, skill):
        skill_comp = Skill(self.effects[self.step])
        skill_comp.caster = skill.caster
        effect = skill.world.create_entity([skill_comp])
        skill_comp.start()
        self.effect = effect
        
    def start(self, skill):
        if len(self.effects) == 0:
            skill.done = True
            return

        self.run_next_effect(skill)
        
    
    def update(self, skill):
        #meh sanity check
        if skill.done:
            return

        #check if effect is done, if so, increment step
        if self.effect.get_component(Skill).done:
            self.step += 1

            if self.step >= len(self.effects):
                skill.done = True
                return

            self.run_next_effect(skill)