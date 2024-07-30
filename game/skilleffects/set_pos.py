from pygame.math import Vector2

from .skilleffect import SkillEffect
from game.components.physics.physics import Physics
from game.components.physics.position import Position
from game.components.actor.actor import Actor

class SetPos(SkillEffect):
    """Will always result in an airborne state"""
    def __init__(self, pos, relative=True):
        super().__init__()
        self.pos = pos
        self.relative = relative
    
    def start(self, skill):
        skill.done = True
        
        phys = skill.target.get_component(Physics)
        position = skill.target.get_component(Position)
        actor = skill.target.get_component(Actor)
        
        pos = position.pos + self.pos.elementwise() * Vector2(actor.facing_dir, 1) if self.relative else self.pos
        
        position.set_pos(pos)
        phys.dislodge()