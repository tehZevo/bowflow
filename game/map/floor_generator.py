from pygame.math import Vector2

from game.components.player_spawn import PlayerSpawn
from game.components.physics.foothold import Foothold
from game.components.spawner import Spawner

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