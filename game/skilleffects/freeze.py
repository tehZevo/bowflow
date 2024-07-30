from .skilleffect import SkillEffect
from game.components.physics.physics import Physics

from game.constants import DT

class Freeze(SkillEffect):
    def __init__(self, time=1):
        super().__init__()
        self.time = time
    
    def start(self, skill):
        #TODO: prevent physics updates flag on physics
        
        phys = skill.target.get_component(Physics)
        phys.prevent_updates = True
    
    def update(self, skill):
        self.time -= DT

        if self.time <= 0:
            phys = skill.target.get_component(Physics)
            phys.zero_velocity()
            phys.prevent_updates = False
            skill.done = True
