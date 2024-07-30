import pygame

from game.ecs import Component
from game.data.stats import Stats
from ..physics.physics import Physics
from .damage_listener import DamageListener
from .death_listener import DeathListener
from .stats_listener import StatsListener
from ..physics.physics_state_listener import PhysicsStateListener

class Actor(Component, PhysicsStateListener):
    def __init__(self):
        super().__init__()

        self.action = None
        self.next_action = None
        self.facing_dir = 1

        self.stats = Stats(hp=100, mp=100)
        self.requirements = [Physics]
    
    def on_physics_state_changed(self, state):
        #cancel current action when entering rope state
        if state.physics.on_rope:
            self.act(None, force=True)

    def damage(self, amount, source=None):
        self.stats.hp -= amount

        for listener in self.entity.get_all_components(DamageListener):
            listener.on_damage(amount, source)
        
        for listener in self.entity.get_all_components(StatsListener):
            listener.on_stats_changed(self.stats)
        
    def begin_action(self, action):
        self.action = action
        if self.action is not None:
            action.start(self.entity)

    def end_action(self):
        self.action.end(self.entity)
        self.action = None

    def use_skill(self, skilldef, level=1, override_direction=None):
        from game.actions.use_skill import UseSkill

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
            for listener in self.entity.get_all_components(DeathListener):
                listener.on_death()
                
            self.entity.remove()
            
        if self.action is not None:
            self.action.update(self.entity)
        
            if self.action.done:
                self.end_action()
                
                if self.next_action is not None:
                    self.begin_action(self.next_action)
                    self.next_action = None