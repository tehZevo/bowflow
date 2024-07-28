#TODO: cleanup imports
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

from game.game import Game

#TODO: fixes to try for pygbag:
#- extract pygame_gui 0.6.12 directly to the game folder
#- write handler using 0.6.9 logic (listen for events)

#TODO: pixelate
# import sys, platform
# if sys.platform == "emscripten":
#     platform.window.canvas.style.imageRendering = "pixelated"

#TODO: save key binds across plays
#TODO: foothold chain creator

async def main():
    game = Game()
    game.setup()

    await game.run()

asyncio.run(main())