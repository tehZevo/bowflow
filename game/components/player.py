import pygame
from pygame.math import Vector2

from ..ecs.component import Component
from .physics import Physics
from .actor import Actor
from .position import Position
from .level_up_listener import LevelUpListener
from .level_up_effect import LevelUpEffect
from ..actions import Move, Jump
from ..data.skill_list import skill_list
from ..data.exp_calcs import calc_player_exp, skill_points_per_level

def pressed_binds(bind_map):
    pressed = pygame.key.get_pressed()
    binds = [bind for key, bind in bind_map.items() if pressed[key]]
    return binds

class Player(Component, LevelUpListener):
    def __init__(self, player_data):
        super().__init__()
        self.player_data = player_data
    
    def get_pressed_binds(self):
        actions = pressed_binds(self.player_data.action_binds)
        skills = pressed_binds(self.player_data.skill_binds)
        return actions, skills

    def on_level_up(self, level):
        #TODO: screen wipe on level up would be cool
        print(f"level up! ({self.player_data.level})")
        self.player_data.skill_points += skill_points_per_level(level)
        print("plus", skill_points_per_level(level), "skill point(s)!")

        self.world.create_entity([
            LevelUpEffect(self.entity)
        ])
        
    def give_exp(self, exp):
        print(f"+{exp} exp")
        self.player_data.exp += exp
        exp_tnl = calc_player_exp(self.player_data.level)
        while self.player_data.exp >= exp_tnl:
            self.player_data.exp -= exp_tnl
            self.player_data.level += 1
            exp_tnl = calc_player_exp(self.player_data.level)

            for listener in self.entity.get_all_components(LevelUpListener):
                listener.on_level_up(self.player_data.level)

    def use_skill(self, skill_name, move_dir):
        actor = self.get_component(Actor)

        if skill_name not in skill_list:
            print("unknown skill:", skill_name)
            return

        if skill_name not in self.player_data.skill_allocations:
            print("player does not have skill:", skill_name)
            return
        
        #get level from allocations
        skill_level = self.player_data.skill_allocations[skill_name]
        if skill_level == 0:
            print("player has skill", skill_name, "level 0, not using.")
            return

        skill = skill_list[skill_name]        
        actor.use_skill(skill, level=skill_level, override_direction=move_dir)
            
    def update(self):
        actions, skills = self.get_pressed_binds()

        #TODO: only jump on press (make hold not jump so player has to time it?)
        #TODO: this might require adding a flag to action binds that means "only update on press"
        #TODO: same with skills -- allow buffering but require an extra press

        actor = self.get_component(Actor)
        phys = self.get_component(Physics)
        
        move_dir = ("move_right" in actions) - ("move_left" in actions)

        #prioritize skills over other actions
        if len(skills) > 0:
            skill_name = list(skills)[0]
            self.use_skill(skill_name, move_dir)
            return
        
        if phys.on_ground and "jump" in actions:
            actor.act(Jump(0.15))
        
        if phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 100))
        
        if not phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 1000))
