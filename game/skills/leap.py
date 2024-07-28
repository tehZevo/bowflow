from game.skilleffects.leap_effect import LeapEffect
from .skilldef import SkillDef

def scaling(ratio):
    return [LeapEffect()]

leap = SkillDef(
    scaling,
    use_time=0.5,
    on_ground=False,
    bufferable=False,
    max_level=1,
)