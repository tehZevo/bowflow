import math

from pygame.math import Vector2

from .skilldef import SkillDef
from ..skilleffects import Damage, ForEachTarget, WithSelfTarget
from ..skilleffects.set_pos import SetPos
from ..skilleffects.chain import Chain
from ..skilleffects.freeze import Freeze
from ..skilleffects.target_methods import TargetBox

def scaling(ratio):
    power = math.floor(20 + ratio)

    #TODO: create Async skilleffect that runs the effect and immediately sets done=True
    
    effect = Chain([
        WithSelfTarget(
            apply=[lambda: SetPos(Vector2(0, 3))]
        ),
        #TODO: hold player in place while using
        ForEachTarget(
            in_a=TargetBox(Vector2(0, -1.5), Vector2(5, 3), max_targets=6),
            apply=[lambda: Damage(power)]
        ),
        WithSelfTarget(
            apply=[lambda: Freeze(0.5)]
        ),
    ])

    return [effect]

acrobatics = SkillDef(
    scaling,
    use_time=0.5,
    on_ground=True,
    in_air=False,
    max_level=3,
    combo=True
)