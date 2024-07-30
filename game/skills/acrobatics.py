import math

from pygame.math import Vector2

from .skilldef import SkillDef
from ..skilleffects import Damage, ForEachTarget, WithSelfTarget
from ..skilleffects.set_pos import SetPos
from ..skilleffects.chain import Chain
from ..skilleffects.target_methods import TargetBox

def scaling(ratio):
    power = math.floor(20 + ratio)

    #TODO: create chain skill effect that waits for each effect to be done before starting the next one
    #TODO: these parallel effects may technically work due to skill effect entity creation order
    # but if not, impl the above chain skill effect
    
    effect = Chain([
        WithSelfTarget(
            apply=[lambda: SetPos(Vector2(0, 3))]
        ),
        #TODO: hold player in place while using
        ForEachTarget(
            in_a=TargetBox(Vector2(0, -1.5), Vector2(5, 3), max_targets=6),
            apply=[lambda: Damage(power)]
        )
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