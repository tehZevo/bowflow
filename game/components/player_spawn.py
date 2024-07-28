from game.ecs import Component

class PlayerSpawn(Component):
    """Marker for placing player after map generation"""
    def __init__(self):
        super().__init__()