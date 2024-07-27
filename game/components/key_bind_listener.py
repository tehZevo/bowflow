
class KeyBindListener:
    def __init__(self):
        super().__init__()
    
    #TODO: for now, we need one function for both so player can short circuit skills before actions
    #TODO: also need to handle multiple actions at once (e.g. to resolve move direction)
    def on_key_binds(self, actions, skills):
        raise NotImplementedError