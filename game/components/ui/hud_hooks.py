from game.ecs import Component
from ..actor.damage_listener import DamageListener
from ..actor.death_listener import DeathListener
from ..actor.stats_listener import StatsListener
from ..actor.level_up_listener import LevelUpListener
from ..actor.player_data_listener import PlayerDataListener

from game.data.exp_calcs import calc_player_exp

class HudHooks(Component, DamageListener, DeathListener, StatsListener, LevelUpListener, PlayerDataListener):
    def __init__(self, hud):
        super().__init__()
        self.hud = hud
        
    def init(self):
        #TODO: initial update
        pass

    def on_stats_changed(self, stats):
        print("hey", stats)
        self.hud.hp_bar.set_percent(stats.hp / stats.max_hp)
        self.hud.mp_bar.set_percent(stats.mp / stats.max_mp)
    
    def on_player_data_changed(self, player_data):
        exp_tnl = calc_player_exp(player_data.level)
        self.hud.exp_bar.set_percent(player_data.exp / exp_tnl)
        self.hud.exp_text.text = f"{player_data.exp}/{exp_tnl}"
    
    def on_level_up(self, leve):
        #TODO?
        pass
    
    def on_damage(self, amount, source):
        #TODO
        pass
    
    def on_death(self):
        #TODO?
        pass