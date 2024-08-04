import random

from pygame.math import Vector2

from game.components.player_spawn import PlayerSpawn
from game.components.physics.foothold import Foothold
from game.components.portal import Portal
from game.components.physics.position import Position
from game.map.objects.map_boundary import MapBoundary
from game.map.objects.foothold_stack import FootholdStack
from game.map.objects.foothold_chain import FootholdChain
from game.map.mapdef import MapDef
from game.utils import bezier

# def foothold_chain(world, points):
#     if len(points) < 2:
#         return
    
#     start = points[0]
#     footholds = []

#     last_foothold = None
    
#     for end in points[1:]:
#         fh_comp = Foothold(start, end)

#         if last_foothold is not None:
#             fh_comp.prev = last_foothold
#             last_foothold.next = fh_comp

#         foothold = world.create_entity([fh_comp])
#         last_foothold = fh_comp
#         footholds.append(foothold)
        
#         start = end
    
#     return footholds

#TODO: reimpl as class that extends FootholdChain
# def foothold_bezier(world, a, b, c, d, num_points=10):
#     ts = [i / (num_points - 1) for i in range(num_points)] #TODO: confirm -1 is correct
#     points = [bezier(a, b, c, d, t) for t in ts]
    
#     return foothold_chain(world, points)

#TODO: rename to map generator
#TODO: accept mapdef
def generate_floor(world):
    mapdef = MapDef()#TODO

    floor = MapBoundary(Vector2(50, 20)).create(world, mapdef)

    portal = world.create_entity([
        Portal(),
    ])

    # foothold_bezier(world, Vector2(20, 1), Vector2(23, -1), Vector2(28, 1), Vector2(30, 3))

    stack_footholds = FootholdStack(Vector2(2, 0), Vector2(48, 20), 4, 2, with_spawners=True).create(world, mapdef)
    
    floor.add_component(PlayerSpawn())
    portal_pos = stack_footholds[-1].get_component(Foothold).calc_position(random.random())
    portal.get_component(Position).set_pos(portal_pos)