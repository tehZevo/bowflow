from dataclasses import dataclass

@dataclass
class PlayerData:
    skill_binds: dict #TODO
    action_binds: dict #TODO
    skill_allocations: dict
    skill_points: int