import pygame

from ..ecs.component import Component
from .physics import Physics
from .actor import Actor
from ..actions import Move, Jump
from ..data.skill_list import skill_list

from ..keybinds import ActionBind, SkillBind

#TODO: this feels backwards and inefficient for large bind maps but pygame doesnt seem to let you iterate over pressed keys
def pressed_binds(bind_map):
    pressed = pygame.key.get_pressed()
    binds = [bind for key, bind in bind_map.items() if pressed[key]]
    actions = set([bind.action_name for bind in binds if isinstance(bind, ActionBind)])
    skills = set([bind.skill_name for bind in binds if isinstance(bind, SkillBind)])
    return actions, skills

class Player(Component):
    def __init__(self):
        super().__init__()
        self.keybinds = {
            pygame.K_LEFT: ActionBind("move_left"),
            pygame.K_RIGHT: ActionBind("move_right"),
            pygame.K_UP: ActionBind("move_up"),
            pygame.K_DOWN: ActionBind("move_down"),
            pygame.K_c: ActionBind("jump"),
            pygame.K_d: SkillBind("leap"),
            pygame.K_z: SkillBind("attack"),
        }

    def update(self):
        action_binds, skill_binds = pressed_binds(self.keybinds)
        # print(action_binds, skill_binds)

        #TODO: only jump on press (make hold not jump so player has to time it?)
        #TODO: this might require adding a flag to action binds that means "only update on press"
        #TODO: same with skills -- allow buffering but require an extra press

        actor = self.get_component(Actor)
        phys = self.get_component(Physics)
        
        move_dir = ("move_right" in action_binds) - ("move_left" in action_binds)

        #prioritize skills over other actions
        if len(skill_binds) > 0:
            skill_name = list(skill_binds)[0]
            skill = skill_list[skill_name] #TODO: check for errors
            actor.use_skill(skill, override_direction=move_dir)
            
            return
        
        if phys.on_ground and "jump" in action_binds:
            actor.act(Jump(0.15))
        
        if phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 100))
        
        if not phys.on_ground and move_dir != 0:
            actor.act(Move(move_dir / 1000))
