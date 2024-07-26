import random

from ..ecs.component import Component
from .actor import Actor
from .physics import Physics
from ..actions import Move

class Monster(Component):
    def __init__(self):
        super().__init__()
        self.target = None
        self.state = "idle"
        self.move_dir = 0

    def init(self):
        self.get_component(Physics).stay_on_footholds = True

    def update_idle(self):
        actor = self.get_component(Actor)
        actor.act(Move(self.move_dir / 200))
        
        if random.random() < 1/100:
            self.move_dir = random.randint(-1, 1)
    
    def update(self):
        #TODO: target if player hits

        if self.state == "idle":
            self.update_idle()
            