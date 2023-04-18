import sys, os, random
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from kivy.core.window import Window

EPSILON = float(5)
BUFFER = float(20)

class Ladder(InstructionGroup):
    def __init__(self, margin_side, margin_bottom, layer_spacing, i):
        super(Ladder, self).__init__()
        self.i = i
        self.margin_bottom = margin_bottom
        self.layer_spacing = layer_spacing
        self.x_center = margin_side + random.randint(0, Window.width - margin_side - BUFFER)
        left_line = Line(points=(self.x_center - BUFFER, margin_bottom + layer_spacing * i, self.x_center - BUFFER, margin_bottom + layer_spacing * (i+1)), width = 5)
        right_line = Line(points=(self.x_center + BUFFER, margin_bottom + layer_spacing * i, self.x_center + BUFFER, margin_bottom + layer_spacing * (i+1)), width = 5)
        center_line1 = Line(points=(self.x_center - BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*1, self.x_center + BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*1), width = 5)
        center_line2 = Line(points=(self.x_center - BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*2, self.x_center + BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*2), width = 5)
        center_line3 = Line(points=(self.x_center - BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*3, self.x_center + BUFFER, margin_bottom + layer_spacing * i + (layer_spacing * (i+1)-layer_spacing*i)/4*3), width = 5)
        self.add(left_line)
        self.add(right_line)
        self.add(center_line1)
        self.add(center_line2)
        self.add(center_line3)
        
    def bounding_box(self):
        return (self.x_center - BUFFER, self.margin_bottom + self.layer_spacing * self.i, self.x_center + BUFFER, self.margin_bottom + self.layer_spacing * (self.i+1))

class BackgroundDisplay(InstructionGroup):
    def __init__(self):
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
        self.ladder_locs = set() #set of (x, y_bottom, y_top)
        for i in range(len(self.layers)-1):
            for _ in range(2):
                this_ladder = Ladder(self.margin_side, self.margin_bottom, self.layer_spacing, i)
                self.add(this_ladder)
                self.ladders.append(this_ladder)
                self.ladder_locs.add((0.5*(this_ladder.bounding_box()[0] + this_ladder.bounding_box()[2]), this_ladder.bounding_box()[1], this_ladder.bounding_box()[3]))
    
    def get_margin_side(self):
        return self.margin_side
    
    def get_margin_bottom(self):
        return self.margin_bottom
    
    def get_layer_spacing(self):
        return self.layer_spacing
    
    def get_buffer(self):
        return BUFFER

    def can_begin_climbing(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        # TODO - make this take into account the width of ladders once ladder isn't just a line
        can_climb = False
        for loc in self.ladder_ends('B'):
            if ((abs(pos[0]-loc[0])**2 + abs(pos[1]-loc[1])**2)**0.5 < BUFFER):
                can_climb = True
                break
        return can_climb
    
    def can_begin_descending(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        can_descend = False
        for loc in self.ladder_ends('T'):
            if ((abs(pos[0]-loc[0])**2 + abs(pos[1]-loc[1])**2)**0.5 < BUFFER):
                can_descend = True
                break
        return can_descend

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        # TODO - make this take into account the width of ladders once ladder isn't just a line
        can_climb = False
        
        for loc in self.ladder_locs:
            if (abs(pos[0]-loc[0]) < BUFFER and pos[1] < loc[2] and pos[1] > loc[1] - EPSILON):
                can_climb = True
                break
        return can_climb
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        can_descend = False
        for loc in self.ladder_locs:
            if (abs(pos[0]-loc[0]) < BUFFER and pos[1] - EPSILON < loc[2] and pos[1] > loc[1]):
                can_descend = True
                break
        return can_descend
    
    # B for bottom, T for top
    def distance_to_ladder_end(self, pos, which_end):
        closest_y_distance = float('inf')
        ladder_ends = self.ladder_ends(which_end)
        for loc in ladder_ends:
            closest_y_distance = min(closest_y_distance, abs(pos[1]-loc))
        return closest_y_distance

    
    # B for bottom, T for top
    def ladder_ends(self, which_end):
        end_idx = 1 if which_end == 'B' else 2
        return [loc[end_idx] for loc in self.ladder_locs]
    
    def get_start_position_height(self):
        return max(self.ladder_ends('T'))

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self):
        pass #TODO
