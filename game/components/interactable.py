
class Interactable:
    def __init__(self):
        super().__init__()
    
    def on_interact(self, entity):
        raise NotImplementedError