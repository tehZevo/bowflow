import pygame
import pygame_gui

def skill_image_path(skill_name):
    return "game/assets/images/skills/" + skill_name + ".png"

def create_skill_icon(skill_name, container, rect):
    surf = pygame.image.load(skill_image_path(skill_name))
    img = pygame_gui.elements.ui_image.UIImage(rect, surf, container=container)
    return img

def skill_button(pos, skill_name, container, tree, callback=lambda: None):
    #TODO: add callback for button that upgrades skill
    surf = pygame.image.load(skill_image_path(skill_name))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((pos.x, pos.y), (32, 32)),
        text='',
        container=container,
        command=callback,
    )
    pygame_gui.elements.ui_image.UIImage(
        pygame.Rect(pos.x, pos.y, 32, 32),
        surf,
        container=container,
        parent_element=button
    )
    return button