import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.elements import UIWindow, UILabel

from game.data.skill_list import skill_list
from ..constants import SKILL_LEVEL_COST
from .skill_button import SkillButton

def job_skills_ui(skills, y, container, tree, player_data):
    for x, skill in enumerate(skills):
        if skill is None:
            continue

        def closure(skill):
            def callback():
                #resolve skill and check level
                max_level = skill_list[skill].max_level #TODO: handle errors
                if player_data.get_skill_level(skill) >= max_level:
                    return
                if player_data.skill_points < SKILL_LEVEL_COST:
                    return
                
                player_data.upgrade_skill(skill)

            SkillButton(Vector2(x * 32, y * 32), skill, container, callback=callback)
        closure(skill)
        
class SkillTreeWindow:
    def __init__(self, tree, player_data):
        #TODO: how to open window centered or remember last position?
        self.window = UIWindow(pygame.Rect((64, 64), (300, 500)), window_display_title="Skills")
        
        job_skills_ui(tree.job1_skills, 3, self.window, tree, player_data)
        job_skills_ui(tree.job2_skills, 2, self.window, tree, player_data)
        job_skills_ui(tree.job3_skills, 1, self.window, tree, player_data)
        job_skills_ui(tree.job4_skills, 0, self.window, tree, player_data)
        
        #TODO: why anchors no work
        self.skill_points_label = UILabel(relative_rect=pygame.Rect(0, 0, 200, 32), container=self.window, text="", anchors={"botom": "bottom", "left": "left"})
        
        self.update(player_data)
        
    def update(self, player_data):
        self.skill_points_label.set_text(f"Skill points remaining: {player_data.skill_points}")