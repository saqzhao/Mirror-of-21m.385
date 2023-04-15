import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from kivy.core.window import Window

class BackgroundDisplay(InstructionGroup):
    def __init__(self) -> None:
        super(BackgroundDisplay, self).__init__()
        self.margin_side = Window.width / 10
        self.margin_bottom = Window.height / 10
        self.layer_spacing = Window.height / 8
        self.layers = []
        for i in range(5):
            this_line = Line(points=(self.margin_side, self.margin_bottom + self.layer_spacing * i, Window.width - self.margin_side, self.margin_bottom + self.layer_spacing * i), width = 6)
            self.add(this_line)
            self.layers.append(this_line)

        # self.ladders = []
        # for layer in self.layers:
        #     for i in range(2)

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        pass #TODO
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        pass #TODO

    def on_resize(self, win_size):
        pass #TODO
