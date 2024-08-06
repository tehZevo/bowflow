import random

from .map_layout import MapLayout
from .objects.map_boundary2 import MapBoundary
from .objects.platform import Platform

from game.components.player_spawn import PlayerSpawn
from game.components.physics.foothold import Foothold
from game.components.portal import Portal
from game.components.physics.position import Position

#TODO: maybe move this to layout class
def generate_layout(width, height, features=[], mandatory_features=[], num_features=10, max_places=1000):
    layout = MapLayout(width, height)
    
    for Feature in mandatory_features:
        feature = Feature()
        if not feature.try_place(layout, None):
            return None
        layout.features.append(feature)

    placed = 0
    for i in range(max_places):
        print("place attempt", i)
        Feature = random.choice(features)
        feature = Feature()
        if feature.try_place(layout, None):
            layout.features.append(feature)
            placed += 1
            print("success, placed", Feature.__name__)
        else:
            print("failed to place", Feature.__name__)
        if placed >= num_features:
            break
    
    return layout

def generate_onto_world(layout, world, mapdef):
    for feature in layout.features:
        feature.generate_entities(layout, world, mapdef)
    
def layout_generator_test(world, mapdef):
    from game.map.seaside_city import seaside_city

    layout = generate_layout(50, 30, [Platform], [MapBoundary], 30, 1000)
    generate_onto_world(layout, world, mapdef)

    #TODO: place portals as a feature/on grid or something instead
    footholds = world.get_all_components(Foothold)
    spawn_fh = random.choice(footholds)
    portal_fh = random.choice(footholds)
    spawn_fh.entity.add_component(PlayerSpawn())
    portal_pos = portal_fh.calc_position(random.random())

    portal = world.create_entity([Portal(seaside_city)])
    portal.get_component(Position).set_pos(portal_pos)