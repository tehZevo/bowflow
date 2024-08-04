from pygame.math import Vector2

from game.ecs import Component
from ..physics.position import Position
from game.components.ui.text import Text
from game.components.ui.box import Box
from game.components.key_bind_listener import KeyBindListener
from game.components.graphics.image import Image

#TODO: wrap
#TODO: multi-cell items?

class GridMenu(Component, KeyBindListener):
    def __init__(self, items={}, cancelable=True):
        super().__init__()
        self.items = items
        self.cursor_pos = Vector2(0, 0)
        self.ents = []
        self.cancelable = cancelable

        self.cursor_image = None

    def items_sorted_by_axis(self, axis, filter_by, reversed=False):
        entries = [(k[axis], v) for k, v in self.items.items() if k[1 - axis] == filter_by]
        entries.sort(key=lambda e: e[0], reverse=reversed)
        return entries

    def move_cursor(self, axis, dir):
        start = self.cursor_pos.x if axis == 0 else self.cursor_pos.y
        filter_by = self.cursor_pos.y if axis == 0 else self.cursor_pos.x
        found = None
        
        for i, item in self.items_sorted_by_axis(axis, filter_by, dir < 0):
            if dir > 0 and i > start:
                found = i
                print("found", found)
                break
            elif dir < 0 and i < start:
                found = i
                print("found", found)
                break
            
        if found is not None:
            if axis == 0:
                self.cursor_pos.x = found
            else:
                self.cursor_pos.y = found
        
        #update cursor pos
        #TODO: make relative to menu pos
        self.cursor_image.get_component(Position).set_pos(self.cursor_pos * 16)

    def on_key_binds(self, binds):
        if "move_up" in binds.pressed_actions:
            self.move_cursor(1, -1)
        if "move_down" in binds.pressed_actions:
            self.move_cursor(1, 1)
        if "move_left" in binds.pressed_actions:
            self.move_cursor(0, -1)
        if "move_right" in binds.pressed_actions:
            self.move_cursor(0, 1)
        if "select" in binds.pressed_actions:
            self.select()
        if "back" in binds.pressed_actions and self.cancelable:
            self.close()
        
    def select(self):
        self.items[(int(self.cursor_pos.x), int(self.cursor_pos.y))].select(self)

    def create(self):
        box = self.world.create_entity([
            Box(Vector2(0, 0), Vector2(10, 16)),
        ])
        self.ents.append(box)

        self.cursor_image = self.world.create_entity([
            Image("game/assets/images/grid_cursor.png")
        ])
        self.ents.append(self.cursor_image)

        for (x, y), item in self.items.items():
            item.create(self, Vector2(x * 16, y * 16))
        
    def close(self):
        #TODO hmm...
        from game.components.ui.ui_manager import UIManager
        self.world.get_all_components(UIManager)[0].close_menu()
        
    def destroy(self):
        #TODO: remove all our ents and self
        for ent in self.ents:
            ent.remove()
        
        for item in self.items.values():
            item.destroy(self)
            
        self.entity.remove()