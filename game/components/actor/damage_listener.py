
class DamageListener:
    def __init__(self):
        super().__init__()
    
    def on_damage(self, amount, source=None):
        raise NotImplementedError