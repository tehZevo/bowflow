import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel

def skill_image_path(skill_name):
    return "game/assets/images/skills/" + skill_name + ".png"

class SkillButton:
    def __init__(self, pos, skill_name, container, callback=lambda: None):
        surf = pygame.image.load(skill_image_path(skill_name))
        rect = pygame.Rect(pos.x, pos.y, 32, 32)
        
        button = UIButton(
            relative_rect=rect,
            text="",
            container=container,
            command=callback,
        )

        UIImage(
            relative_rect=rect,
            image_surface=surf,
            container=container,
            parent_element=button,
        )

        self.level_label = UILabel(rect, container=container, text="")
        
        self.button = button

        self.update(2)
    
    def update(self, level):
        #TODO: where to get max info from
        max = "???"
        self.level_label.set_text(f"{level}/{max}")
