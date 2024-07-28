
class PlayerDataListener:
    def __init__(self):
        super().__init__()
    
    def on_player_data_changed(self, player_data):
        raise NotImplementedError