from .skilleffect import SkillEffect
from ..components.actor.actor import Actor
from ..components.physics.physics import Physics
from ..components.physics.position import Position
from game.actions import Busy
from game.constants import DT, DEBUG_TARGETS

class Carry(SkillEffect):
    def __init__(self, target_method, time=1):
        """Any targets caught in target area are carried with the caster"""
        super().__init__()
        self.target_method = target_method
        self.time = time
        self.time_remaining = time
        self.carried_ents = []
    
    def release_carry(self):
        for ent in self.carried_ents:
            actor = ent.get_component(Actor)
            phys = ent.get_component(Physics)
            actor.act(None, force=True)
            if phys.on_ground:
                phys.state.vel = 0

    def update(self, skill):
        #TODO: store list of entities currently being carried?
        #TODO: prolly impl by copying velocity to target
        #TODO: carry ground/air but not rope-state targets
        #TODO: actually, just disallow targeting rope-state
        
        #TODO: allow carry midair
        caster_phys = skill.caster.get_component(Physics)
        if not caster_phys.on_ground:
            skill.done = True
            self.release_carry()
            return

        self.time_remaining -= DT

        if self.time_remaining <= 0:
            skill.done = True
            self.release_carry()
            return
        
        if DEBUG_TARGETS:
            self.target_method.debug(skill.caster, time=0)
        
        #release current carried ents
        self.release_carry()

        #grab new targets
        self.carried_ents = self.target_method.get_targets(skill.caster)
        
        #set their vel to caster vel
        for ent in self.carried_ents:
            phys = ent.get_component(Physics)
            if not phys.on_ground:
                continue
            
            phys.state.vel = caster_phys.state.vel