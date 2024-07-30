import math

from pygame.math import Vector2

from .skilldef import SkillDef
from ..skilleffects import Damage, ForEachTarget
from ..skilleffects.target_methods import TargetBox

def scaling(ratio):
    power = math.floor(10 + ratio)

    effect = ForEachTarget(
        in_a=TargetBox(Vector2(4, 0), Vector2(8, 4), max_targets=4),
        apply=[lambda: Damage(power, 4)]
    )

    return [effect]

magibolt = SkillDef(
    scaling,
    use_time=0.5,
    max_level=3,
)