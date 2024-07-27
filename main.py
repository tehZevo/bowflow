import time
import asyncio
import pygame, sys
from pygame.math import Vector2
import pygame_gui
import i18n

from game.ecs import World
from game.components import Physics, Player, Position, Sprite, Renderable, Foothold, Camera, Actor, Monster, SkillTreeUI
from game.constants import DT
from game.data.skill_tree import SkillTree

from game.ui.skill_button import skill_button

#TODO: save key binds across plays

def job_skills_ui(skills, y, container, tree):
    for x, skill in enumerate(skills):
        if skill is None:
            continue
    
        skill_button(Vector2(x * 32, y * 32), skill, container, tree)

def skill_tree_ui(tree, container):
    job_skills_ui(tree.job1_skills, 3, container, tree)
    job_skills_ui(tree.job2_skills, 2, container, tree)
    job_skills_ui(tree.job3_skills, 1, container, tree)
    job_skills_ui(tree.job4_skills, 0, container, tree)

async def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 640))
    pygame.display.set_caption("Hello World")
    manager = pygame_gui.UIManager((1280, 640))

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (16, 16)),
                                             text='',
                                             manager=manager)

    world = World()

    playerComp = Player()
    
    player = world.create_entity([
        Position(Vector2(1, 1)),
        Physics(),
        Sprite(offset=Vector2(-1/2, -1)),
        Actor(),
        Player(),
    ])

    for i in range(10):
        monster = world.create_entity([
            Position(Vector2(10 + i - 5, 1)),
            Physics(),
            Sprite(),
            Actor(),
            Monster(),
        ])
        monster.get_component(Sprite).set_image("monster.png")

    #TODO: foothold chain creator
    foothold = world.create_entity([
        Foothold(Vector2(-10, -10), Vector2(30, -10))
    ])

    foothold = world.create_entity([
        Foothold(Vector2(3, -8), Vector2(8, -8))
    ])

    foothold = world.create_entity([
        Foothold(Vector2(12, -6), Vector2(16, -6))
    ])

    foothold = world.create_entity([
        Foothold(Vector2(7, -7), Vector2(12, -9))
    ])
    
    camera = world.create_entity([
        Position(),
        Camera(target=player)
    ])

    skill_tree = SkillTree()

    skill_tree_ui(skill_tree, None)
    
    camera_comp = camera.get_component(Camera)

    player.get_component(Sprite).set_image("player.png")

    # clock = pygame.time.Clock()
    last_time = time.time()
    while True:
        # time_delta = clock.tick(60)/1000.0
        screen.fill((200, 255, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
            
            manager.process_events(event)

        manager.update(DT)

        world.update()

        for renderable in world.get_all_components(Renderable):
            renderable.render(screen, camera_comp)
        
        manager.draw_ui(screen)
        
        pygame.display.update()
        dt = time.time() - last_time
        last_time = time.time()
        await asyncio.sleep(DT - dt) #TODO: uncap framerate?

asyncio.run(main())