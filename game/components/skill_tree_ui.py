from pygame.math import Vector2

from ..ecs import Component
from .sprite import Sprite
from .position import Position

def skill_image_path(skill_name):
    return "game/assets/images/skills/" + skill_name + ".png"

def create_skill_icon(world, skill_name, position):
    sprite = Sprite(skill_image_path(skill_name))
    bg = Sprite(skill_image_path("skillbg"))
    
    world.create_entity([bg, Position(position)])
    world.create_entity([sprite, Position(position)])

class SkillTreeUI(Component):
    def __init__(self, skill_tree):
        super().__init__()
        self.skill_tree = skill_tree
    
    def create_job_icons(self, y, skills):
        for x, skill in enumerate(skills):
            if skill is None:
                continue
            
            create_skill_icon(self.world, skill, Vector2(x * 64, y * 64))

    def init(self):
        tree = self.skill_tree
        self.create_job_icons(3, tree.job1_skills)
        self.create_job_icons(2, tree.job2_skills)
        self.create_job_icons(1, tree.job3_skills)
        self.create_job_icons(0, tree.job4_skills)