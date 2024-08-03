from .menu_item import MenuItem

class OpenMenu(MenuItem):
    def __init__(self, text, menu_creator):
        super().__init__(text)
        self.menu_creator = menu_creator
    
    def select(self, menu):
        from game.components.ui.ui_manager import UIManager
        new_menu = self.menu_creator(menu)
        #TODO: make it possible to close the current menu before opening a new one?
        menu.world.get_all_components(UIManager)[0].open_menu(new_menu)