
class SkillDef:
    def __init__(self, effects=lambda ratio: [], max_level=1, use_time=1, bufferable=True, on_ground=True, in_air=True):
        """
        effects function = given a float (0..1) based on ratio of current level to max level, determine a list of effects to apply
        ratio will be 0 when level is 1 and will be 1 when level is maxed
        """
        self.effects = effects
        self.use_time = use_time
        self.bufferable = bufferable
        self.on_ground = on_ground
        self.in_air = in_air
        self.max_level = max_level