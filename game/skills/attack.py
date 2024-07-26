from pygame.math import Vector2

from .skilldef import SkillDef
from ..skilleffects import Damage, ForEachTarget
from ..skilleffects.target_methods import TargetBox

effect = ForEachTarget(
    in_a=TargetBox(Vector2(4, 0), Vector2(8, 4), max_targets=4),
    apply=[Damage(30)]
)

attack = SkillDef([effect], use_time=0.5)