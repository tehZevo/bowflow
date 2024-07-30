from .action import Action
from ..constants import DT
from ..components.skill import Skill
from ..components.physics.physics import Physics
from ..components.actor import Actor

class UseSkill(Action):
    def __init__(self, skilldef, level=1, cast_direction=None):
        super().__init__()
        self.skilldef = skilldef
        self.level = level
        self.skill_time = self.skilldef.use_time
        self.cast_direction = cast_direction
        #protection against non-[-1/1] cast directions
        self.cast_direction = None if cast_direction is None else 1 if cast_direction > 0 else -1 if cast_direction < 0 else None
        self.bufferable = skilldef.bufferable
        self.level = level
        
        self.locked = self.skilldef.combo
    
    def start(self, entity):
        #bail on combo lock
        #TODO: how to prevent these from preventing other actions like movement?
        if self.locked:
            self.done = True
            return
            
        #physics state checks, bail if failed

        #ground/air checks
        phys = entity.get_component(Physics)
        if not self.skilldef.in_air and phys.in_air:
            self.done = True
            return
        if not self.skilldef.on_ground and phys.on_ground:
            self.done = True
            return
        if not self.skilldef.on_rope and phys.on_rope:
            self.done = True
            return

        #allow "buffered" turns before cast
        if self.cast_direction is not None:
            entity.get_component(Actor).facing_dir = self.cast_direction
        
        #apply level to get effects
        effects = self.skilldef.effects(self.level / self.skilldef.max_level)
        
        for effect in effects:
            skill_comp = Skill(effect)
            skill_comp.caster = entity
            skill = entity.world.create_entity([skill_comp])
            skill_comp.start()
    
    def update(self, entity):
        self.skill_time -= DT
        if self.skill_time <= 0:
            self.done = True