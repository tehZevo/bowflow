from game.ecs import Component

from game.components.graphics.sprite import Sprite

#TODO: mapdef
class Portal(Component):
    def __init__(self):
        super().__init__()
    
    def init(self):
        self.get_component(Sprite).set_image("game/assets/images/portal.png")