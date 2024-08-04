from pygame.math import Vector2

from game.ecs import Component
from ..physics.physics import Physics
from ..physics.position import Position
from ..physics.rope import Rope
from ..interactable import Interactable
from ..graphics import Sprite
from ..graphics.level_up_effect import LevelUpEffect
from .actor import Actor
from .level_up_listener import LevelUpListener
from .player_data_listener import PlayerDataListener
from game.components.key_bind_listener import KeyBindListener
from game.actions import Move, Jump, Climb, JumpOffRope
from game.actions.jump_down import JumpDown
from game.data.skill_list import skill_list
from game.data.exp_calcs import calc_player_exp, skill_points_per_level
from game.constants import INTERACT_RADIUS, ROPE_GRAB_DISTANCE, ROPE_REGRAB_DELAY, DT
from game.components.physics.physics_states.ground_state import GroundState
import game.sprites

class Player(Component, LevelUpListener, KeyBindListener):
    def __init__(self, player_data):
        super().__init__()
        self.player_data = player_data
        self.move_dir = 0
        self.climb_dir = 0
        self.rope_regrab_delay = 0
        self.requirements = [Actor, Physics, Sprite]
    
    def init(self):
        sprite = self.get_component(Sprite)
        sprite.set_spritedef(game.sprites.magibowman)
        sprite.anchor_bottom()

        self.alert_player_data_listeners()
    
    def attempt_interact(self):
        my_pos = self.get_component(Position).pos
        for interactable in self.world.get_all_components(Interactable):
            other_pos = interactable.get_component(Position).pos
            dist = my_pos.distance_to(other_pos)
            if dist < INTERACT_RADIUS:
                interactable.on_interact(self.entity)

    def on_key_binds(self, binds):
        phys = self.get_component(Physics)
        pos = self.get_component(Position)
        actor = self.get_component(Actor)

        if not phys.on_rope and len(binds.pressed_skills) > 0:
            self.use_skill(list(binds.pressed_skills)[0], self.move_dir)
            return
        
        self.move_dir = ("move_right" in binds.held_actions) - ("move_left" in binds.held_actions)
        self.climb_dir = ("move_up" in binds.held_actions) - ("move_down" in binds.held_actions)

        if not phys.on_rope and "move_up" in binds.held_actions and self.rope_regrab_delay <= 0:
            for rope in self.world.get_all_components(Rope):
                if rope.distance(pos.pos) < ROPE_GRAB_DISTANCE:
                    phys.grab_rope(rope)
        
        if phys.on_ground and "move_down" in binds.held_actions:
            for rope in self.world.get_all_components(Rope):
                if rope.distance(pos.pos) < ROPE_GRAB_DISTANCE:
                    phys.grab_rope(rope)

        if phys.on_ground and "jump" in binds.pressed_actions:
            if "move_down" in binds.held_actions:
                actor.act(JumpDown())
            else:
                actor.act(Jump(0.15))
        
        if phys.on_rope and "jump" in binds.pressed_actions and self.move_dir != 0:
            self.rope_regrab_delay = ROPE_REGRAB_DELAY
            actor.act(JumpOffRope(self.move_dir))
        
        if phys.on_rope and "jump" in binds.held_actions and self.climb_dir > 0:
            self.use_skill("ascend", self.move_dir)
        
        if phys.on_ground and "interact" in binds.pressed_actions:
            self.attempt_interact()
        
    
    def on_level_up(self, level):
        #TODO: screen wipe on level up would be cool
        print(f"level up! ({self.player_data.level})")
        self.player_data.skill_points += skill_points_per_level(level)
        print("plus", skill_points_per_level(level), "skill point(s)!")

        self.world.create_entity([
            LevelUpEffect(self.entity)
        ])
    
    def alert_player_data_listeners(self):
        for listener in self.entity.get_all_components(PlayerDataListener):
            listener.on_player_data_changed(self.player_data)

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
        
        self.alert_player_data_listeners()
        
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
        #TODO: only jump on press (make hold not jump so player has to time it?)
        #TODO: this might require adding a flag to action binds that means "only update on press"
        #TODO: same with skills -- allow buffering but require an extra press

        actor = self.get_component(Actor)
        phys = self.get_component(Physics)

        if phys.on_ground and self.move_dir != 0:
            actor.act(Move(self.move_dir / 150))
        
        if not phys.on_ground and self.move_dir != 0:
            actor.act(Move(self.move_dir / 1000))

        if phys.on_rope and self.climb_dir != 0:
            actor.act(Climb(self.climb_dir))

        #TODO: make rope grab logic in air based on intersection, but on ground, based on distance
        if self.rope_regrab_delay > 0:
            self.rope_regrab_delay -= DT