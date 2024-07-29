from .skilleffect import SkillEffect
from ..components.actor.actor import Actor
from ..components.physics.physics import Physics
from ..components.physics.position import Position
from game.actions import Busy
from game.constants import DT

class Push(SkillEffect):
    def __init__(self, distance, time=1, relative_to_caster=False):
        """Relative to caster modifies the push distance so the push ends relative to the caster"""
        super().__init__()
        self.distance = distance
        self.direction = None
        self.time = time
        self.relative_to_caster = relative_to_caster
        self.time_remaining = self.time
    
    def start(self, skill):
        target_phys = skill.target.get_component(Physics)
        cast_dir = skill.caster.get_component(Actor).facing_dir
        target_actor = skill.target.get_component(Actor)

        self.direction = cast_dir

        if self.relative_to_caster:
            caster_x = skill.caster.get_component(Position).pos.x
            target_x = skill.target.get_component(Position).pos.x
            push_end = caster_x + self.distance * self.direction
            self.distance = abs(push_end - target_x)

        #TODO: how to handle midair push (e.g. diving)?
        #TODO: a midair push can become a grounded push if physics state transitions!
        
        if not target_phys.on_ground:
            skill.done = True
            return
        
        target_actor.act(Busy(), force=True)
    
    def end_push(self, skill):
        skill.done = True
        target_actor.act(None, force=True)
        target_phys.state.vel = 0
        if self.relative_to_caster:
            print("target push end")

    def update(self, skill):
        target_phys = skill.target.get_component(Physics)
        target_actor = skill.target.get_component(Actor)

        #TODO: prevent falling off
        
        if not target_phys.on_ground:
            skill.done = True
            target_actor.act(None, force=True)
            return
        
        self.time_remaining -= DT

        if self.time_remaining <= 0:
            skill.done = True
            target_actor.act(None, force=True)
            target_phys.state.vel = 0
            if self.relative_to_caster:
                print("target push end")
            return
        
        target_phys.state.vel = self.distance / self.time * self.direction * DT