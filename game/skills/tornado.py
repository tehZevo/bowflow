import math

from pygame.math import Vector2

from .skilldef import SkillDef
from ..skilleffects import Damage, ForEachTarget
from ..skilleffects.with_self_target import WithSelfTarget
from ..skilleffects.target_methods import TargetBox
from ..skilleffects.force import Force
from game.skillreqs.require_height import RequireHeight

def scaling(ratio):
    power = math.floor(10 + ratio)
    
    self_force = WithSelfTarget([lambda: Force(Vector2(0, 0.1))])# cancel_y_vel=True)])
    
    damage = ForEachTarget(
        in_a=TargetBox(Vector2(0, -1.5), Vector2(7, 3), max_targets=6),
        apply=[lambda: Damage(power)]
    )

    return [self_force, damage]

tornado = SkillDef(
    scaling,
    use_time=1,
    max_level=3,
    on_ground=False,
    in_air=True,
    requirements=[RequireHeight(1.8)]
)