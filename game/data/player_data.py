from dataclasses import dataclass, field
from collections import defaultdict

from ..constants import SKILL_LEVEL_COST

@dataclass
class PlayerData:
    skill_binds: dict = field(default_factory=lambda: dict)
    action_binds: dict = field(default_factory=lambda: dict)
    skill_allocations: dict = field(default_factory=lambda: dict)
    skill_points: int = 0

    def get_skill_level(self, skill):
        #TODO: do we want to check for skill validitity here?

        if skill not in self.skill_allocations:
            return 0
        
        return self.skill_allocations[skill]

    def upgrade_skill(self, skill):
        #TODO: do we want to check for skill validitity here?

        if self.skill_points < SKILL_LEVEL_COST:
            raise ValueError("Not enough skill points")
        
        #avoiding defaultdict so constructor calls/deserialization to playerdata are simpler
        if skill not in self.skill_allocations:
            self.skill_allocations[skill] = 0
        
        self.skill_allocations[skill] += 1
        self.skill_points -= SKILL_LEVEL_COST

        print("upgraded", skill, "to level", self.skill_allocations[skill])