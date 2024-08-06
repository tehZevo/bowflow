import time
import asyncio

import pygame, sys
from pygame.math import Vector2

from game.ecs import World
from game.components.physics import Physics, Position, Foothold
from game.components.graphics import Renderable, Camera
from game.components.ui import HudHooks
from game.components.actor import Player
from game.components.key_bind_monitor import KeyBindMonitor
from game.components.player_spawn import PlayerSpawn
from game.components.game_master import GameMaster
from game.components.ui.ui_manager import UIManager
from game.components.ui.hud import HUD
from game.components.ui.box import Box
from game.components.ui.text import Text
from game.constants import DT
from game.data.skill_tree import SkillTree
from game.data.player_data import PlayerData
# from game.map.beach import beach
from game.map.layout_generator_test import layout_generator_test
from game.constants import PPU, WIDTH_UNITS, HEIGHT_UNITS, SCREEN_SCALE


class Game:
    def __init__(self):
        self.interrupt_loop = False
        self.paused = False
    
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_UNITS * PPU * SCREEN_SCALE, HEIGHT_UNITS * PPU * SCREEN_SCALE))
        self.canvas = pygame.surface.Surface((WIDTH_UNITS * PPU, HEIGHT_UNITS * PPU))
        pygame.display.set_caption("Project Bow Flow")

        self.player_data = PlayerData(
            skill_binds = {
                pygame.K_d: "leap",
                pygame.K_z: "magibolt",
                pygame.K_q: "rush",
                pygame.K_w: "acrobatics",
                pygame.K_e: "tornado",
            },
            action_binds = {
                pygame.K_LEFT: "move_left",
                pygame.K_RIGHT: "move_right",
                pygame.K_UP: "move_up",
                pygame.K_DOWN: "move_down",
                pygame.K_c: "jump",
                # pygame.K_k: "keys", #TODO: action bindings
                pygame.K_l: "skills",
                pygame.K_SPACE: "interact",
                pygame.K_ESCAPE: "back",
                pygame.K_RETURN: "select",
            },
            skill_allocations={
                "magibolt": 1,
                "leap": 1,
                "ascend": 1,
                "rush": 3,
                "acrobatics": 3,
                "tornado": 3,
            },
            skill_points=100
        )

        self.skill_tree = SkillTree()

        self.ui_world = World()
        
        self.ui_world.create_entity([GameMaster(self)])

        self.ui_world.create_entity([
            KeyBindMonitor(self.player_data),
            UIManager(),
        ])

        self.hud = HUD()
        self.ui_world.create_entity([
            self.hud
        ])
        
        self.create_new_world(layout_generator_test)

    def change_map(self, mapdef):
        self.next_mapdef = mapdef
        self.interrupt_loop = True

    def create_new_world(self, mapdef):
        self.world = World()

        self.world.create_entity([GameMaster(self)])

        mapdef.generate(self.world)

        player_comp = Player(self.player_data)

        self.player = self.world.create_entity([
            Position(Vector2(1, 1)),
            HudHooks(self.hud),
            KeyBindMonitor(self.player_data),
            player_comp,
        ])

        self.camera = self.world.create_entity([Camera(target=self.player)])

        spawn_foothold = self.world.get_all_components(PlayerSpawn)[0].get_component(Foothold)
        self.player.get_component(Physics).move_to_foothold(spawn_foothold)

        self.camera_comp = self.camera.get_component(Camera)
        self.camera.get_component(Position).set_pos(self.player.get_component(Position).pos)
        
    async def run(self):
        while True:
            last_time = time.time()
            t = 0
            while not self.interrupt_loop:
                self.canvas.fill((200, 200, 200))
                t += 0.01
                if t > 1:
                    t = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if not self.paused:
                    self.world.update()
                self.ui_world.update()

                #TODO: use sprite batches in the future for performance boost
                for renderable in self.world.get_all_components(Renderable):
                    renderable.render(self.canvas, self.camera_comp)
                
                for renderable in self.ui_world.get_all_components(Renderable):
                    renderable.render(self.canvas)

                scaled_canvas = pygame.transform.scale(self.canvas, self.screen.get_size())
                self.screen.blit(scaled_canvas, (0, 0))

                pygame.display.update()
                dt = time.time() - last_time
                last_time = time.time()

                await asyncio.sleep(max(0, DT - dt)) #TODO: uncap framerate?
                # await asyncio.sleep(0)

            #change maps
            self.create_new_world(self.next_mapdef)
            self.next_mapdef = None
            self.interrupt_loop = False

            await asyncio.sleep(0)