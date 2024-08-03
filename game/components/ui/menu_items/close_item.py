from .lambda_item import LambdaItem

class CloseItem(LambdaItem):
    def __init__(self, text="Close"):
        super().__init__(text, action=lambda menu: None, close_on_select=True)