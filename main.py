import time
import asyncio
import math

import pygame, sys
from pygame.math import Vector2
import pygame_gui
import i18n

from game.ecs import World
from game.components import Physics, Player, Position, Sprite, Renderable, Foothold, Camera, Actor, Monster
from game.constants import DT
from game.data.skill_tree import SkillTree
from game.data.player_data import PlayerData

from game.ui.skill_tree_window import skill_tree_window


from game.data.exp_calcs import calc_player_exp, calc_mob_exp

for level in range(1, 100):
    p_exp = calc_player_exp(level)
    m_exp = calc_mob_exp(level)
    kills = round(p_exp / m_exp)
    print(level, "player TNL:", p_exp, "mob:", m_exp, "kills:", kills)

#TODO: save key binds across plays

async def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 640))
    pygame.display.set_caption("Project Bow Flow")
    manager = pygame_gui.UIManager((1280, 640))

    world = World()

    player_data = PlayerData(
        skill_binds = {
            pygame.K_d: "leap",
            pygame.K_z: "magibolt",
        },
        action_binds = {
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_c: "jump",
        },
        skill_allocations={
            "magibolt": 1
        },
        skill_points=100
    )

    player_comp = Player(player_data)
    
    player = world.create_entity([
        Position(Vector2(1, 1)),
        Physics(),
        Sprite(offset=Vector2(-1/2, -1)),
        Actor(),
        player_comp,
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

    skill_tree_window(Vector2(32, 32), skill_tree, player_data)
    
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