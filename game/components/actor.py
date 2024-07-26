import pygame

from ..ecs.component import Component
from ..data.stats import Stats

class Actor(Component):
    def __init__(self):
        super().__init__()

        self.action = None
        self.next_action = None
        self.facing_dir = 1

        self.stats = Stats(hp=100, mp=100)
    
    def begin_action(self, action):
        self.action = action
        action.start(self.entity)

    def end_action(self):
        self.action.end(self.entity)
        self.action = None

    def act(self, action, force=False):
        if self.action is None:
            self.begin_action(action)
        elif self.action.interruptible or force:
            self.end_action()
            self.begin_action(action)
        else:
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