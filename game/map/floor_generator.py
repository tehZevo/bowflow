import random

from pygame.math import Vector2

from game.components.player_spawn import PlayerSpawn
from game.components.physics.foothold import Foothold
from game.components.spawner import Spawner
from game.components.portal import Portal
from game.components.physics.position import Position
from game.components.graphics.sprite import Sprite
from game.components.physics.wall import Wall
from game.components.physics.rope import Rope

#TODO: function for spawners
def foothold_stack(world, start_pos, width, height, n_platforms=2, ropes=2):
    diff = height / n_platforms
    for i in range(n_platforms):
        start = start_pos + Vector2(0, diff * i)
        end = start + Vector2(width, 0)

        foothold = world.create_entity([Foothold(start, end)])
        
        if i == 0:
            continue

        for _ in range(ropes):
            rope_pos = start + (end - start) * random.random()
            rope_length = diff / 2 + diff / 2 * random.random()
            rope = world.create_entity([Rope(rope_pos, rope_length)])

#TODO: rename map generator
def generate_floor(world):
    foothold = world.create_entity([
        Foothold(Vector2(-10, -10), Vector2(30, -10)),
        Spawner(),
    ])

    foothold.add_component(PlayerSpawn())

    foothold = world.create_entity([
        Foothold(Vector2(3, -8), Vector2(8, -8)),
        Spawner(),
    ])

    foothold = world.create_entity([
        Foothold(Vector2(12, -6), Vector2(16, -6)),
        Spawner(),
    ])

    foothold = world.create_entity([
        Foothold(Vector2(7, -7), Vector2(12, -9)),
        Spawner(),
    ])

    wall = world.create_entity([
        Wall(Vector2(-2, -7), Vector2(-2, -12), 1)
    ])

    rope = world.create_entity([
        Rope(Vector2(14, -6), 3)
    ])

    portal = world.create_entity([
        Portal(),
    ])

    foothold_stack(world, Vector2(-2, -5), 20, 20, 5, 2)

    portal_pos = foothold.get_component(Foothold).calc_position(random.random()) + Vector2(0, 1)
    portal.get_component(Position).set_pos(portal_pos)