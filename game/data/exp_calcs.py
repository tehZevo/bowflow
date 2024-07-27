from ..constants import MAX_LEVEL, PLAYER_EXP_START, PLAYER_EXP_END, MOB_KILLS_START, MOB_KILLS_END
from game.utils import round_sigfigs

#offset needed to align exp funcs
def calc_scaling(start, end, levels, offset=2): #-2 for alignment
    return (end / start) ** (1 / (levels - offset))

def calc_player_exp(level):
    scaling = calc_scaling(PLAYER_EXP_START, PLAYER_EXP_END, MAX_LEVEL)
    x = PLAYER_EXP_START * (scaling ** (level - 1))
    return round_sigfigs(x, 2)

def calc_mob_exp(level):
    scaling = calc_scaling(MOB_KILLS_START, MOB_KILLS_END, MAX_LEVEL)
    kills = MOB_KILLS_START * (scaling ** (level - 1))
    player_exp = calc_player_exp(level)
    exp_per_mob = round(player_exp / kills)
    return round_sigfigs(exp_per_mob, 2)