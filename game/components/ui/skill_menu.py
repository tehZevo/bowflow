from pygame.math import Vector2

from ..physics.position import Position
from game.components.ui.box import Box
from game.components.ui.grid_menu import GridMenu
from game.components.ui.menu_items.skill_upgrade_item import SkillUpgradeItem

class SkillMenu(GridMenu):
    def __init__(self, skill_tree):
        self.skill_tree = skill_tree
        super().__init__(items=self.build_items())

    def build_item_row(self, items, y, skills):
        for i, skill in enumerate(skills):
            if skill is None:
                continue
            items[(i, y)] = SkillUpgradeItem(skill)

    def build_items(self):
        items = {}
        self.build_item_row(items, 0, self.skill_tree.job4_skills)
        self.build_item_row(items, 1, self.skill_tree.job3_skills)
        self.build_item_row(items, 2, self.skill_tree.job2_skills)
        self.build_item_row(items, 3, self.skill_tree.job1_skills)
        return items