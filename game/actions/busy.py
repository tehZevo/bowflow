from .action import Action

class Busy(Action):
    """
    An action that does nothing. Must be manually overridden by .act(..., force=True)
    Be careful when using busy as it causes you to not be able to tell which skill the player is currently using
    """
    def __init__(self):
        super().__init__()