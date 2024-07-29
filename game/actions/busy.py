from .action import Action

class Busy(Action):
    """An action that does nothing. Must be manually overridden by .act(..., force=True)"""
    def __init__(self):
        super().__init__()