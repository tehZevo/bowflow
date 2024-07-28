import random

from game.ecs import Component
from game.actions import Move
from game.data.exp_calcs import calc_mob_exp
from ..physics.physics import Physics
from ..physics.position import Position
from .actor import Actor
from .damage_listener import DamageListener
from .death_listener import DeathListener

class Monster(Component, DamageListener, DeathListener):
    def __init__(self):
        super().__init__()
        self.target = None
        self.last_attacker = None
        self.move_dir = 0
        
        #TODO: dont hardcode level, use mobdef or something
        self.level = 100

    def init(self):
        self.get_component(Physics).stay_on_footholds = True

    def on_damage(self, amount, source):
        self.target = source
        
        if source is not None:
            self.last_attacker = source
    
    def on_death(self):
        from .player import Player

        if self.last_attacker is not None:
            player = self.last_attacker.get_component(Player)
            if player is not None:
                player.give_exp(calc_mob_exp(self.level))

    def update_idle(self):
        actor = self.get_component(Actor)
        actor.act(Move(self.move_dir / 200))
        
        if random.random() < 1/100:
            self.move_dir = random.randint(-1, 1)
    
    def update_follow(self):
        if random.random() < 1/50:
            target_pos = self.target.get_component(Position).pos
            diff = target_pos - self.get_component(Position).pos
        
            self.move_dir = -1 if diff.x < 0 else 1
        
        self.get_component(Actor).act(Move(self.move_dir / 200))

    def update(self):
        
        if self.target is None:
            self.update_idle()
        else:
            self.update_follow()
            