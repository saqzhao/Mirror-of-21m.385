import sys, os, random
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
        for i in range(7):
            this_line = Line(points=(self.margin_side, self.margin_bottom + self.layer_spacing * i, Window.width - self.margin_side, self.margin_bottom + self.layer_spacing * i), width = 6)
            self.add(this_line)
            self.layers.append(this_line)

        self.ladders = []
        for i in range(len(self.layers)-1):
            for _ in range(2):
                x = self.margin_side + random.randint(0, Window.width - self.margin_side)
                this_ladder = Line(points=(x, self.margin_bottom + self.layer_spacing * i, x, self.margin_bottom + self.layer_spacing * (i+1)), width = 6)
                self.add(this_ladder)
                self.ladders.append(this_ladder)

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        pass #TODO
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        pass #TODO

    def on_resize(self, win_size):
        pass #TODO
