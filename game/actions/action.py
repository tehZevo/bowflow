
class Action:
    def __init__(self):
        self.done = False
        self.interruptible = False

    def start(self, entity):
        """Called when an actor begins this action"""
        pass
    
    def update(self, entity):
        """Called every step that the actor is performing this action"""
        pass

    def end(self, entity):
        """Called when the actor ends this action"""
        pass