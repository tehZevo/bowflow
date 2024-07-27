from ..ecs.component import Component
from .damage_listener import DamageListener
from .death_listener import DeathListener
from .stats_listener import StatsListener
from .level_up_listener import LevelUpListener
from .player_data_listener import PlayerDataListener

from ..data.exp_calcs import calc_player_exp

class HudHooks(Component, DamageListener, DeathListener, StatsListener, LevelUpListener, PlayerDataListener):
    def __init__(self, hud):
        super().__init__()
        self.hud = hud
        
    def init(self):
        #TODO: initial update
        pass

    def on_stats_changed(self, stats):
        #TODO
        self.hud.hp_bar.max_value = stats.max_hp
        self.hud.hp_bar.update(stats.hp)
        self.hud.mp_bar.max_value = stats.max_mp
        self.hud.mp_bar.update(stats.mp)
    
    def on_player_data_changed(self, player_data):
        exp_tnl = calc_player_exp(player_data.level)
        self.hud.exp_bar.max_value = exp_tnl
        self.hud.exp_bar.update(player_data.exp)
        self.hud.level_label.update(player_data.level)
    
    def on_level_up(self, leve):
        #TODO?
        pass
    
    def on_damage(self, amount, source):
        #TODO
        pass
    
    def on_death(self):
        #TODO?
        pass