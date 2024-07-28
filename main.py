import time
import asyncio
import math

import pygame, sys
from pygame.math import Vector2
import pygame_gui
import i18n

from game.ecs import World
from game.components.physics import Physics, Position, Foothold
from game.components.graphics import Sprite, Renderable, Camera
from game.components.ui import HudHooks
from game.components.actor import Player, Actor, Monster
from game.components.key_bind_monitor import KeyBindMonitor
from game.components.spawner import Spawner
from game.components.player_spawn import PlayerSpawn
from game.constants import DT
from game.data.skill_tree import SkillTree
from game.data.player_data import PlayerData
from game.map.floor_generator import generate_floor
from game.ui.skill_tree_window import SkillTreeWindow
from game.ui.hud import Hud

#TODO: save key binds across plays

async def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 640))
    pygame.display.set_caption("Project Bow Flow")
    manager = pygame_gui.UIManager((1280, 640), "game/assets/theme.json")

    world = World()
    
    hud = Hud()

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
            # pygame.K_k: "keys", #TODO: action bindings
            pygame.K_l: "skills",
        },
        skill_allocations={
            "magibolt": 1
        },
        skill_points=100
    )

    #TODO: foothold chain creator
    generate_floor(world)

    player_comp = Player(player_data)
    
    player = world.create_entity([
        Position(Vector2(1, 1)),
        Physics(),
        Sprite(offset=Vector2(-1/2, -1)),
        Actor(),
        HudHooks(hud),
        KeyBindMonitor(player_data),
        player_comp,
    ])

    camera = world.create_entity([
        Position(),
        Camera(target=player)
    ])

    spawn_foothold = world.get_all_components(PlayerSpawn)[0].get_component(Foothold)
    player.get_component(Physics).move_to_foothold(spawn_foothold)

    skill_tree = SkillTree()

    skill_window = SkillTreeWindow(skill_tree, player_data)
    
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