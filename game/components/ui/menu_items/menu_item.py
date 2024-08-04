
class MenuItem:
    def __init__(self, text):
        self.text = text
    
    def select(self, menu):
        raise NotImplementedError

    def create(self, menu):
        pass
    
    def destroy(self, menu):
        pass