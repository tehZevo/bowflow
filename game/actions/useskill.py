from .action import Action
from ..constants import DT
from ..components.skill import Skill

class UseSkill(Action):
    def __init__(self, skilldef):
        super().__init__()
        self.skilldef = skilldef
        self.skill_time = self.skilldef.use_time
    
    def start(self, entity):
        for effect in self.skilldef.effects:
            skill_comp = Skill(effect)
            skill_comp.caster = entity
            skill = entity.world.create_entity([skill_comp])
            skill_comp.start()
    
    def update(self, entity):
        self.skill_time -= DT
        if self.skill_time <= 0:
            self.done = True