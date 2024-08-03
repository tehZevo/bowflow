
from game.ecs import Component
from game.components.key_bind_listener import KeyBindListener
from game.components.ui.menu import Menu
from game.components.ui.menu_items.lambda_item import LambdaItem
from game.components.ui.menu_items.close_item import CloseItem
from game.components.game_master import GameMaster
from game.components.actor.player import Player

class UIManager(Component, KeyBindListener):
    def __init__(self):
        super().__init__()
        self.menu_stack = []
    
    def get_active_menu(self):
        if len(self.menu_stack) == 0:
            return None
        
        return self.menu_stack[-1]

    def on_key_binds(self, binds):
        #transfer key binds to active menu
        active_menu = self.get_active_menu()
        if active_menu is not None:
            active_menu.on_key_binds(binds)
            return

        if "back" in binds.pressed_actions:
            #open menu
            #TODO: improve experience of getting player
            player = self.world.get_all_components(GameMaster)[0].game.world.get_all_components(Player)[0]

            give_exp_item = LambdaItem("Exp me!", lambda menu: player.give_exp(100))
            self.menu = Menu([
                give_exp_item,
                CloseItem(),
            ])
            self.open_menu(self.menu)
            
    def open_menu(self, menu):
        self.world.create_entity([menu])
        self.menu_stack.append(menu)
        menu.create()
    
    def close_menu(self):
        menu = self.get_active_menu()
        
        if menu is None:
            return

        menu.destroy()

        self.menu_stack.pop()

        game = self.world.get_all_components(GameMaster)[0].game
        game.paused = False