#TODO: cleanup imports
import asyncio
import math

import pygame
import pygame_gui
import i18n

from game.game import Game

#TODO: fixes to try for pygbag:
#- extract pygame_gui 0.6.12 directly to the game folder
#- write handler using 0.6.9 logic (listen for events)
#- just dont use pygame_gui at all

#TODO: pixelate in chrome
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