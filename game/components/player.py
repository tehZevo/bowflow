import pygame

from ..ecs.component import Component
from .physics import Physics
from .actor import Actor
from ..actions import Move, Jump
from ..data.skill_list import skill_list

def pressed_binds(bind_map):
    pressed = pygame.key.get_pressed()
    binds = [bind for key, bind in bind_map.items() if pressed[key]]
    return binds

class Player(Component):
    def __init__(self):
        super().__init__()
        self.skill_binds = {
            pygame.K_d: "leap",
            pygame.K_z: "attack",
        }
        self.action_binds = {
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_c: "jump",
        }

    def update(self):
        actions = pressed_binds(self.action_binds)
        skills = pressed_binds(self.skill_binds)

        #TODO: only jump on press (make hold not jump so player has to time it?)
        #TODO: this might require adding a flag to action binds that means "only update on press"
        #TODO: same with skills -- allow buffering but require an extra press

        actor = self.get_component(Actor)
        phys = self.get_component(Physics)
        
        move_dir = ("move_right" in actions) - ("move_left" in actions)

        #prioritize skills over other actions
        if len(skills) > 0:
            skill_name = list(skills)[0]
            skill = skill_list[skill_name] #TODO: check for errors
            actor.use_skill(skill, override_direction=move_dir)
            
            return
        
        if phys.on_ground and "jump" in actions:
            actor.act(Jump(0.15))
        
        if phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 100))
        
        if not phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 1000))
