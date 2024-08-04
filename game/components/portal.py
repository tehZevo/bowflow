from game.ecs import Component

from game.components.interactable import Interactable
from game.components.graphics.image import Image
from game.components.game_master import GameMaster

#TODO: use mapdef
class Portal(Component, Interactable):
    def __init__(self):
        super().__init__()

        self.requirements = [Image]
    
    def init(self):
        image = self.get_component(Image)
        image.set_image("game/assets/images/portal.png")
        image.anchor_bottom()

    def on_interact(self, entity):
        self.world.get_all_components(GameMaster)[0].game.change_map()