from .menu_item import MenuItem

class LambdaItem(MenuItem):
    def __init__(self, text, action=lambda menu: None, close_on_select=True):
        super().__init__(text)
        self.action = action
        self.close_on_select = close_on_select

    def select(self, menu):
        self.action(menu)
        
        if self.close_on_select:
            menu.close()