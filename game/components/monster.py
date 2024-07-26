import random

from ..ecs.component import Component
from .actor import Actor
from .physics import Physics
from .position import Position
from ..actions import Move
from .damage_listener import DamageListener

class Monster(Component, DamageListener):
    def __init__(self):
        super().__init__()
        self.target = None
        self.move_dir = 0

    def init(self):
        self.get_component(Physics).stay_on_footholds = True

    def on_damage(self, amount, source):
        self.target = source

    def update_idle(self):
        actor = self.get_component(Actor)
        actor.act(Move(self.move_dir / 200))
        
        if random.random() < 1/100:
            self.move_dir = random.randint(-1, 1)
    
    def update_follow(self):
        if random.random() < 1/50:
            target_pos = self.target.get_component(Position).pos
            diff = target_pos - self.get_component(Position).pos
        
            self.move_dir = -1 if diff.x < 0 else 1
        
        self.get_component(Actor).act(Move(self.move_dir / 200))

    def update(self):
        
        if self.target is None:
            self.update_idle()
        else:
            self.update_follow()
            