from game.ecs import Component

class Renderable(Component):
    def __init__(self):
        super().__init__()
    
    def render(self, screen, camera=None):
        """Render to the screen with the given camera (no camera = assumed screen space)"""
        pass