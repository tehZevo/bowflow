from game.ecs import Component

from game.components.interactable import Interactable
from game.components.graphics.sprite import Sprite
from game.components.game_master import GameMaster

#TODO: mapdef
class Portal(Component, Interactable):
    def __init__(self):
        super().__init__()
    
    def init(self):
        self.get_component(Sprite).set_image("game/assets/images/portal.png")

    def on_interact(self, entity):
        self.world.get_all_components(GameMaster)[0].game.change_map()