import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.core import ObjectID

from pygame_gui.elements import UIStatusBar, UILabel

class HudBar:
    def __init__(self, rect, max_value, value=None, include_percent=False, name=None, class_id=None):
        object_id = ObjectID(class_id=class_id) if class_id is not None else None
        self.max_value = max_value
        self.value = value if value is not None else max_value
        self.name = name
        self.include_percent = include_percent

        self.bar = UIStatusBar(rect, object_id=object_id)
        self.label = UILabel(rect, text="", object_id=ObjectID(class_id="@hud_bar_text"))

        self.update(self.value)
    
    def build_label_text(self):
        text = ""
        if self.name is not None:
            text += self.name + ": "
        text += f"{self.value} / {self.max_value}"
        if self.include_percent:
            text += f" ({round(self.value / self.max_value, 2)}%)"
        return text

    def update(self, value):
        self.value = value
        self.label.set_text(self.build_label_text())
        
        self.bar.percent_full = self.value / self.max_value
