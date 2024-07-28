from pygame.math import Vector2

from game.ecs import Component

class GameMaster(Component):
    def __init__(self, game):
        super().__init__()
        
        self.game = game
    
    #TODO: accept mapdef
    def change_map(self):
        
