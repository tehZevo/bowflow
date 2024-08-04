import asyncio
import math

import pygame
import i18n

from game.game import Game

#TODO: pixelate in chrome
# import sys, platform
# if sys.platform == "emscripten":
#     platform.window.canvas.style.imageRendering = "pixelated"

#TODO: save key binds across plays

async def main():
    game = Game()
    game.setup()

    await game.run()

asyncio.run(main())