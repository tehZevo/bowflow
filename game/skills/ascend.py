from .skilldef import SkillDef
from ..skilleffects.ascend_effect import AscendEffect

#ascend is a passive skill that results in an active skill being used lol...
def scaling(ratio):
    return [AscendEffect()]

ascend = SkillDef(
    scaling,
    use_time=0.5,
    on_ground=False,
    in_air=False,
    on_rope=True,
    bufferable=False,
    max_level=1,
)