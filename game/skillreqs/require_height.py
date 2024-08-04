from pygame.math import Vector2

from game.utils import intersect
from game.components.physics.physics import Physics
from game.components.physics.position import Position 
from game.components.physics.foothold import Foothold

from .skillreq import SkillReq

class RequireHeight(SkillReq):
    def __init__(self, height=2):
        super().__init__()
        self.height = height
    
    def can_use(self, caster):
        phys = caster.get_component(Physics)
        if not phys.in_air:
            return False
        
        pos = caster.get_component(Position).pos
        
        #intersect all footholds, if any hit, fail
        for fh in caster.world.get_all_components(Foothold):
            intersection_pos = intersect(fh.start, fh.end, pos, pos - Vector2(0, self.height))
            if intersection_pos is not None:
                return False
        
        return True
