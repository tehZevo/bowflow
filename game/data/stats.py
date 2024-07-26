from dataclasses import dataclass

#TODO: idk how deep i want to go with stats in this game

@dataclass
class Stats:
    max_hp: int = 100
    max_mp: int = 100
    hp: int = 100
    mp: int = 100