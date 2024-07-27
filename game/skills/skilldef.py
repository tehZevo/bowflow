
class SkillDef:
    def __init__(self, effects=[], use_time=1, bufferable=True, on_ground=True, in_air=True):
        self.effects = effects
        self.use_time = use_time
        self.bufferable = bufferable
        self.on_ground = on_ground
        self.in_air = in_air