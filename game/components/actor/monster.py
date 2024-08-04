import random

import pygame
from pygame.math import Vector2
 
from game.ecs import Component
from game.actions import Move
from game.actions.hitstun import Hitstun
from game.data.exp_calcs import calc_mob_exp
from ..physics.physics import Physics
from ..graphics.sprite import Sprite
from ..physics.position import Position
from .actor import Actor
from .damage_listener import DamageListener
from .death_listener import DeathListener
import game.sprites

class Monster(Component, DamageListener, DeathListener):
    def __init__(self):
        super().__init__()
        self.target = None
        self.last_attacker = None
        self.move_dir = 0
        
        #TODO: dont hardcode level, use mobdef or something
        self.level = 100

        self.requirements = [Actor, Sprite, Position, Physics]

    def init(self):
        self.get_component(Physics).stay_on_footholds = True
        sprite = self.get_component(Sprite)
        #sprite.set_image("game/assets/images/slime.png")
        sprite.set_spritedef(game.sprites.slime)
        sprite.anchor_bottom()

    def on_damage(self, amount, source):
        self.target = source

        hit_sound = pygame.mixer.Sound("game/assets/audio/mob_hit.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(hit_sound)
        
        actor = self.get_component(Actor)
        hitstun_dir = -actor.facing_dir

        if source is not None:
            self.last_attacker = source
            hitstun_dir = source.get_component(Actor).facing_dir
        
        actor.act(Hitstun(hitstun_dir))
    
    def on_death(self):
        from .player import Player

        die_sound = pygame.mixer.Sound("game/assets/audio/mob_die.wav") #TODO: store this somewhere
        pygame.mixer.Sound.play(die_sound)

        if self.last_attacker is not None:
            player = self.last_attacker.get_component(Player)
            if player is not None:
                player.give_exp(calc_mob_exp(self.level))

    def update_idle(self):
        actor = self.get_component(Actor)

        if self.move_dir != 0:
            actor.act(Move(self.move_dir / 200))
        
        
        if random.random() < 1/100:
            self.move_dir = random.randint(-1, 1)
    
    def update_follow(self):
        if random.random() < 1/50:
            target_pos = self.target.get_component(Position).pos
            diff = target_pos - self.get_component(Position).pos
        
            self.move_dir = -1 if diff.x < 0 else 1
        
        if self.move_dir != 0:
            self.get_component(Actor).act(Move(self.move_dir / 200))

    def update(self):
        
        if self.target is None:
            self.update_idle()
        else:
            self.update_follow()
            