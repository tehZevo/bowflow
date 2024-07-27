import pygame

from ..ecs.component import Component
from ..data.stats import Stats
from .damage_listener import DamageListener
from .physics import Physics

class Actor(Component):
    def __init__(self):
        super().__init__()

        self.action = None
        self.next_action = None
        self.facing_dir = 1

        self.stats = Stats(hp=100, mp=100)
    
    def damage(self, amount, source=None):
        self.stats.hp -= amount

        for listener in self.entity.get_all_components(DamageListener):
            listener.on_damage(amount, source)
        
    def begin_action(self, action):
        self.action = action
        action.start(self.entity)

    def end_action(self):
        self.action.end(self.entity)
        self.action = None

    def use_skill(self, skilldef, level=1, override_direction=None):
        from ..actions.useskill import UseSkill

        #ground/air checks
        phys = self.get_component(Physics)
        if not skilldef.in_air and not phys.on_ground:
            return
        if not skilldef.on_ground and phys.on_ground:
            return
        
        dir = override_direction if override_direction is not None else self.facing_dir

        self.act(UseSkill(skilldef, level=level, cast_direction=dir))

    def act(self, action, force=False):
        if self.action is None:
            self.begin_action(action)
        elif self.action.interruptible or force:
            self.end_action()
            self.begin_action(action)
        elif action.bufferable:
            self.next_action = action
            
    def update(self):
        if self.stats.hp <= 0:
            self.entity.remove()
            
        if self.action is not None:
            self.action.update(self.entity)
        
            if self.action.done:
                self.end_action()
                
                if self.next_action is not None:
                    self.begin_action(self.next_action)
                    self.next_action = None