
class TargetMethod:
    def __init__(self):
        super().__init__()
    
    def debug(self, caster):
        """Debug the target method (e.g. spawn a DebugBox)"""
        pass
    
    def get_targets(self, caster):
        raise NotImplementedError