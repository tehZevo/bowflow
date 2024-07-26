import time
import asyncio
import pygame, sys
from pygame.math import Vector2

from game.ecs import World
from game.components import Physics, Player, Position, Sprite, Renderable, Foothold, Camera, Actor, Monster
from game.constants import DT

async def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Hello World")

    world = World()

    playerComp = Player()
    
    player = world.create_entity([
        Position(Vector2(1, 1)),
        Physics(),
        Sprite(),
        Actor(),
        Player(),
    ])

    for i in range(100):
        monster = world.create_entity([
            Position(Vector2(10 + i / 10 - 5, 1)),
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

    camera_comp = camera.get_component(Camera)

    player.get_component(Sprite).set_image("player.png")

    last_time = time.time()
    while True:
        screen.fill((200, 255, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        world.update()

        for renderable in world.get_all_components(Renderable):
            renderable.render(screen, camera_comp)

        pygame.display.update()
        dt = time.time() - last_time
        last_time = time.time()
        await asyncio.sleep(DT - dt) #TODO: uncap framerate?

asyncio.run(main())