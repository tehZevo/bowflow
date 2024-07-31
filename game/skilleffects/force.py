import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from game.components.physics.physics import Physics
from game.components.actor.actor import Actor

class Force(SkillEffect):
    def __init__(self, force):
        super().__init__()
        self.force = force
    
    def start(self, skill):
        skill.done = True
        
        phys = skill.caster.get_component(Physics)
        #skill should only be castable midair, but this is an extra sanity check since we are messing with air velocity
        if not phys.in_air:
            return

        actor = skill.caster.get_component(Actor)

        phys.apply_force(self.force.elementwise() * Vector2(actor.facing_dir, 1))
