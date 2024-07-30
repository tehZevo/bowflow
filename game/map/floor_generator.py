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

from game.utils import bezier

#TODO: function for spawners
def foothold_stack(world, start_pos, width, height, n_platforms=2, ropes=2):
    diff = height / n_platforms
    footholds = []
    for i in range(n_platforms):
        start = start_pos + Vector2(0, diff * i)
        end = start + Vector2(width, 0)

        foothold = world.create_entity([Foothold(start, end)])
        footholds.append(foothold)
        
        if i == 0:
            continue

        for _ in range(ropes):
            rope_pos = start + (end - start) * random.random()
            rope_length = diff / 2 + diff / 2 * random.random()
            rope = world.create_entity([Rope(rope_pos, rope_length)])
    
    return footholds

def foothold_chain(world, points):
    if len(points) < 2:
        return
    
    start = points[0]
    footholds = []

    last_foothold = None
    
    for end in points[1:]:
        fh_comp = Foothold(start, end)

        if last_foothold is not None:
            fh_comp.prev = last_foothold
            last_foothold.next = fh_comp

        foothold = world.create_entity([fh_comp])
        last_foothold = fh_comp
        footholds.append(foothold)
        
        start = end
    
    return footholds

def foothold_bezier(world, a, b, c, d, num_points=10):
    ts = [i / (num_points - 1) for i in range(num_points)] #TODO: confirm -1 is correct
    points = [bezier(a, b, c, d, t) for t in ts]
    
    return foothold_chain(world, points)

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

    foothold_bezier(world, Vector2(20, -9), Vector2(23, -11), Vector2(28, -9), Vector2(30, -7))

    foothold_stack(world, Vector2(-2, -5), 20, 20, 5, 2)

    portal_pos = foothold.get_component(Foothold).calc_position(random.random()) + Vector2(0, 1)
    portal.get_component(Position).set_pos(portal_pos)