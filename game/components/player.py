import pygame

from ..ecs.component import Component
from .position import Position
from .physics import Physics
from .actor import Actor
from ..actions import Move, Jump, UseSkill
from ..skills import leap, attack

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
        keys = pygame.key.get_pressed()
        
        action_binds, skill_binds = pressed_binds(self.keybinds)
        # print(action_binds, skill_binds)
        x = ("move_right" in action_binds) - ("move_left" in action_binds)
        
        #TODO: only jump on press (make hold not jump so player has to time it?)
        #TODO: this might require adding a flag to action binds that means "only update on press"

        phys = self.get_component(Physics)
        pos = self.get_component(Position)

        actor = self.get_component(Actor)

        if "leap" in skill_binds:
            #actor.act(UseSkill(leap, cast_direction=x))
            actor.use_skill(leap, override_direction=x)
        
        if phys.on_ground and "jump" in action_binds:
            actor.act(Jump(0.15))
        
        if phys.on_ground and x != 0:
            actor.act(Move(x / 100))
        
        if not phys.on_ground and x != 0:
            actor.act(Move(x / 1000))

        if "attack" in skill_binds:
            actor.act(UseSkill(attack, cast_direction=x), buffer=False)
            