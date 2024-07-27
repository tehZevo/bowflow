from collections import defaultdict

class SkillTree:
    def __init__(self):
        self.job4_skills = [None, None, "zip"]
        self.job3_skills = ["volley"]
        self.job2_skills = ["double_bolt", None, "rush"]
        self.job1_skills = ["magibolt", "leap"]

        self.allocations = defaultdict(int)
    
    #TODO: upgradable skills
    def upgrade_skill(skill_name):
        self.allocations[skill_name] += 1
