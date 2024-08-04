from game.ecs import Component

from game.components.interactable import Interactable
from game.components.graphics.sprite import Sprite
from game.components.game_master import GameMaster

#TODO: mapdef
class Portal(Component, Interactable):
    def __init__(self):
        super().__init__()

        self.requirements = [Sprite]
    
    def init(self):
        sprite = self.get_component(Sprite)
        sprite.set_image("game/assets/images/portal.png")
        sprite.anchor_bottom()

    def on_interact(self, entity):
        self.world.get_all_components(GameMaster)[0].game.change_map()