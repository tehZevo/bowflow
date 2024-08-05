from pygame.math import Vector2

from game.components.player_spawn import PlayerSpawn
from game.components.physics.foothold import Foothold
from game.components.portal import Portal
from game.components.physics.position import Position
from game.map.objects.map_boundary import MapBoundary
from game.map.mapdef import MapDef

def generator(world, mapdef):
    from .beach import beach

    floor = MapBoundary(Vector2(30, 10)).create(world, mapdef)

    beach_portal = world.create_entity([Portal(beach)])
    city_portal = world.create_entity([Portal(seaside_city)])
    
    beach_fh = Foothold(Vector2(5, 2), Vector2(5+2, 2))
    city_fh = Foothold(Vector2(30-5-2, 2), Vector2(30-2, 2))
    world.create_entity([beach_fh])
    world.create_entity([city_fh])

    beach_portal.get_component(Position).set_pos(beach_fh.calc_position(0.5))
    city_portal.get_component(Position).set_pos(city_fh.calc_position(0.5))

    floor.add_component(PlayerSpawn())

seaside_city = MapDef(name="Seaside City", generator=generator)

