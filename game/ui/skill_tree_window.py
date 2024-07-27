import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.elements.ui_window import UIWindow

from .skill_button import skill_button

def job_skills_ui(skills, y, container, tree):
    for x, skill in enumerate(skills):
        if skill is None:
            continue
    
        skill_button(Vector2(x * 32, y * 32), skill, container, tree)
        
def skill_tree_window(pos, tree):
    window = UIWindow(pygame.Rect(pos, (500, 500)), window_display_title="Skills")
    
    job_skills_ui(tree.job1_skills, 3, window, tree)
    job_skills_ui(tree.job2_skills, 2, window, tree)
    job_skills_ui(tree.job3_skills, 1, window, tree)
    job_skills_ui(tree.job4_skills, 0, window, tree)