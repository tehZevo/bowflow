
class StatsListener:
    def __init__(self):
        super().__init__()
    
    def on_stats_changed(self, stats):
        raise NotImplementedError