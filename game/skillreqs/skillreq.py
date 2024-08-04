
class SkillReq:
    def __init__(self):
        pass

    def can_use(self, caster):
        """Should return true if the caster can use the skill"""
        raise NotImplementedError