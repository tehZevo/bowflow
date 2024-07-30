import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from game.components.physics.physics import Physics
from game.components.actor.actor import Actor
from game.actions.busy import Busy

class AscendEffect(SkillEffect):
    def __init__(self):
        super().__init__()
    
    def start(self, skill):
        phys = skill.caster.get_component(Physics)
        actor = skill.caster.get_component(Actor)

        if not phys.on_rope:
            skill.done = True
            return

        leap_sound = pygame.mixer.Sound("game/assets/audio/leap.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(leap_sound)
        actor = skill.caster.get_component(Actor)
        actor.act(Busy(), force=True)

    
    def update(self, skill):
        phys = skill.caster.get_component(Physics)
        
        if not phys.on_rope:
            skill.done = True
            actor = skill.caster.get_component(Actor)
            #TODO: check if theyre busy first before overriding action..
            # something that knocked them off the rope could have also set an action
            actor.act(None, force=True)
            
            #TODO: this might overwrite something else's velocity modification idk
            if phys.in_air:
                phys.state.vel = Vector2(0, 0.1)

            #TODO: set velocity at end
            return
            
        phys.apply_force(Vector2(0, 2/10.))