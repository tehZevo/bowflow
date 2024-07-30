
class Action:
    def __init__(self):
        self.done = False
        self.interruptible = False
        #whether the actor can set this as the "next action"
        self.bufferable = True

    def start(self, entity):
        """Called when an actor begins this action"""
        pass

    def update(self, entity):
        """Called every step that the actor is performing this action"""
        pass

    def end(self, entity):
        """Called when the actor ends this action"""
        pass