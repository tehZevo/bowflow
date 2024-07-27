import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.elements.ui_window import UIWindow

from .skill_button import skill_button
from game.data.skill_list import skill_list
from ..constants import SKILL_LEVEL_COST

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

            skill_button(Vector2(x * 32, y * 32), skill, container, tree, callback=callback)
        closure(skill)
        
def skill_tree_window(pos, tree, player_data):
    window = UIWindow(pygame.Rect(pos, (500, 500)), window_display_title="Skills")
    
    job_skills_ui(tree.job1_skills, 3, window, tree, player_data)
    job_skills_ui(tree.job2_skills, 2, window, tree, player_data)
    job_skills_ui(tree.job3_skills, 1, window, tree, player_data)
    job_skills_ui(tree.job4_skills, 0, window, tree, player_data)