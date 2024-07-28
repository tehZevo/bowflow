import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from game.components.physics.physics import Physics
from game.components.actor.actor import Actor

class LeapEffect(SkillEffect):
    def __init__(self):
        super().__init__()
    
    def start(self, skill):
        phys = skill.caster.get_component(Physics)
        #skill should only be castable midair, but this is an extra sanity check since we are messing with air velocity
        if not phys.in_air:
            return
        actor = skill.caster.get_component(Actor)

        leap_sound = pygame.mixer.Sound("leap.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(leap_sound)
        
        phys.state.vel.x = 0
        
        phys.apply_force(Vector2(actor.facing_dir / 6, 0.05))

        skill.done = True