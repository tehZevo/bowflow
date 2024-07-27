
class DeathListener:
    def __init__(self):
        super().__init__()
    
    def on_death(self):
        raise NotImplementedError