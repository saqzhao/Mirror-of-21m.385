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
        self.ladder_bottoms = set()
        self.ladder_tops = set()
        for i in range(len(self.layers)-1):
            for _ in range(2):
                x = self.margin_side + random.randint(0, Window.width - self.margin_side)
                this_ladder = Line(points=(x, self.margin_bottom + self.layer_spacing * i, x, self.margin_bottom + self.layer_spacing * (i+1)), width = 6)
                self.add(this_ladder)
                self.ladders.append(this_ladder)
                self.ladder_bottoms.add((x, self.margin_bottom + self.layer_spacing * i))
                self.ladder_tops.add((x, self.margin_bottom + self.layer_spacing * (i+1)))

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        # TODO - make this take into account the width of ladders once ladder isn't just a line
        can_climb = False
        for loc in self.ladder_bottoms:
            if ((abs(pos[0]-loc[0])**2 + abs(pos[1]-loc[1])**2)**0.5 < 20):
                can_climb = True
                break
        return can_climb
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        can_descend = False
        for loc in self.ladder_tops:
            if ((abs(pos[0]-loc[0])**2 + abs(pos[1]-loc[1])**2)**0.5 < 20):
                can_descend = True
                break
        return can_descend

    def on_resize(self, win_size):
        pass #TODO
