from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from .effect import Effect
from .image import Image

class LevelUpEffect(Component):
    """Level up effect for the given entity"""
    def __init__(self, for_entity):
        super().__init__()
        self.for_entity = for_entity
        self.requirements = [Position]

    def init(self):
        pos = self.for_entity.get_component(Position).pos
        pos = pos + Vector2(0, 3)

        self.get_component(Position).set_pos(pos)
        self.entity.add_component(Effect("game/assets/images/level_up.png", time=1))