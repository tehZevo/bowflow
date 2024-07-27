
class LevelUpListener:
    def __init__(self):
        super().__init__()
    
    def on_level_up(self, level):
        raise NotImplementedError