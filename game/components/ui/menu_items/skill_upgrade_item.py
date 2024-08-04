from .menu_item import MenuItem

from game.components.graphics.image import Image
from game.components.physics.position import Position

class SkillUpgradeItem(MenuItem):
    def __init__(self, skill):
        super().__init__(skill)
        self.skill = skill
        self.image = None
        self.bg = None

    def create(self, menu, pos):
        self.image = menu.world.create_entity([
            Position(pos),
            Image(f"game/assets/images/skills/skill_bg.png")
        ])
        self.bg = menu.world.create_entity([
            Position(pos),
            Image(f"game/assets/images/skills/{self.skill}.png")
        ])

    def select(self, menu):
        from game.components.game_master import GameMaster
        from game.components.actor.player import Player
        player = menu.world.get_all_components(GameMaster)[0].game.world.get_all_components(Player)[0]
        player.player_data.upgrade_skill(self.skill)

    def destroy(self, menu):
        self.image.remove()
        self.bg.remove()