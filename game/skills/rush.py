from pygame.math import Vector2

from game.skilleffects.push import Push
from game.skilleffects.carry import Carry
from game.skilleffects.with_self_target import WithSelfTarget
from ..skilleffects import Damage, ForEachTarget
from ..skilleffects.target_methods import TargetBox
from ..skilleffects.chain import Chain
from ..skilleffects.damage import Damage
from ..skilleffects.combo_into import ComboInto
from .skilldef import SkillDef

def scaling(ratio):
    from .acrobatics import acrobatics

    distance = 3 + 4 * ratio
    
    self_push = Chain([
        WithSelfTarget(
            apply=[lambda: Push(distance, time=0.9)]
        ),
        ComboInto(acrobatics),
    ])
    #TODO: want to apply damage here somehow.. maybe make carry not re-find ents every frame?
    mob_carry = Carry(
        target_method=TargetBox(Vector2(0, 1), Vector2(1, 3), max_targets=12),
        time=1
    )
    
    return [self_push, mob_carry]

rush = SkillDef(
    scaling,
    use_time=1,
    on_ground=True,
    in_air=False,
    bufferable=False,
    max_level=3,
)