from .skilleffect import SkillEffect
from game.components.actor.actor import Actor
from game.actions.use_skill import UseSkill

class ComboInto(SkillEffect):
    def __init__(self, skilldefs):
        """Unlocks next useskill action if its skilldef matches ours"""
        super().__init__()
        #coerce to list
        if not type(skilldefs) == list:
            skilldefs = [skilldefs]

        self.skilldefs = skilldefs
    
    def start(self, skill):
        skill.done = True
        
        actor = skill.caster.get_component(Actor)

        if not isinstance(actor.next_action, UseSkill):
            return
        
        use_skill = actor.next_action
        for skilldef in self.skilldefs:
            #TODO: this equality check might get messy later
            if use_skill.skilldef == skilldef:
                use_skill.locked = False
                return
