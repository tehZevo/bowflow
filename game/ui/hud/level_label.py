from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel

class LevelLabel:
    def __init__(self, rect, level=1):
        self.label = UILabel(rect, text="", object_id=ObjectID(class_id="@hud_level_text"))
        self.update(level)
    
    def update(self, level):
        self.level = level
        text = f"Level: {level}"
        self.label.set_text(text)