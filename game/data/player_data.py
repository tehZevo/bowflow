from dataclasses import dataclass, field

@dataclass
class PlayerData:
    skill_binds: dict = field(default_factory=lambda: dict)
    action_binds: dict = field(default_factory=lambda: dict)
    skill_allocations: dict = field(default_factory=lambda: dict)
    skill_points: int = 0