
class SkillDef:
    def __init__(self, effects=lambda ratio: [], max_level=1, use_time=1, bufferable=True, on_ground=True, in_air=True, on_rope=False, combo=False):
        """
        effects function = given a float (0..1) based on ratio of current level to max level, determine a list of effects to apply
        ratio will be 0 when level is 1 and will be 1 when level is maxed
        combo skilldefs will take no action if not unlocked by something (e.g. skilleffect) first
        """
        self.effects = effects
        self.use_time = use_time
        self.bufferable = bufferable
        self.on_ground = on_ground
        self.in_air = in_air
        self.on_rope = on_rope
        self.max_level = max_level
        self.combo = combo