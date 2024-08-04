import pygame
from pygame.math import Vector2

from .skilleffect import SkillEffect
from game.components.physics.physics import Physics
from game.components.actor.actor import Actor

class Force(SkillEffect):
    #TODO: maybe split out vel canceling into its own skilleffect
    def __init__(self, force, cancel_x_vel=False, cancel_y_vel=False):
        super().__init__()
        self.force = force
        self.cancel_x_vel = cancel_x_vel
        self.cancel_y_vel = cancel_y_vel
    
    def start(self, skill):
        skill.done = True
        
        phys = skill.caster.get_component(Physics)
        #skill should only be castable midair, but this is an extra sanity check since we are messing with air velocity
        if not phys.in_air:
            return

        actor = skill.caster.get_component(Actor)

        phys.zero_vel(self.cancel_x_vel, self.cancel_y_vel)
        phys.apply_force(self.force.elementwise() * Vector2(actor.facing_dir, 1))
