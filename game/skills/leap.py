from .skilldef import SkillDef
from ..skilleffects import LeapEffect

leap = SkillDef([
        LeapEffect()
    ],
    use_time=0.5,
    on_ground=False,
    bufferable=False,
)