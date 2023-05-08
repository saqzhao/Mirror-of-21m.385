import sys, os, random
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from imslib.gfxutil import CLabelRect
from kivy.core.window import Window
from kivy.uix.image import Image
from BirdCounter import BirdCounter
from kivy import metrics
from kivy.metrics import Metrics

Y_EPSILON = float(Window.height/150)
X_BUFFER = float(2*Window.width/50)
Y_BUFFER = float(Window.height/37.5)


class Ladder(InstructionGroup):
    def __init__(self, margin_side, margin_bottom, layer_spacing, layer_idx, x_centers_to_avoid = None):
        super(Ladder, self).__init__()
        self.layer_idx = layer_idx
        self.margin_bottom = margin_bottom
        self.margin_side = margin_side
        self.layer_spacing = layer_spacing
        self.num_ladder_rungs = 3
        self.furthest_x_center_loc = int(Window.width - 2*self.margin_side - X_BUFFER - Window.width/33.33)
        self.init_furthest_x_center_loc = self.furthest_x_center_loc
        self.random_number_chosen = random.randint(0, int(self.furthest_x_center_loc))
        self.x_center = self.margin_side + Window.width/100 + self.random_number_chosen
        if x_centers_to_avoid[self.layer_idx] is not None:
            while any((abs(pos-self.x_center) < 3*X_BUFFER) for pos in x_centers_to_avoid[self.layer_idx]):
                self.random_number_chosen = random.randint(0, int(self.furthest_x_center_loc))
                self.x_center = self.margin_side + Window.width/100 + self.random_number_chosen

        self.horiz_lines = []
        self.vert_lines_left = []
        self.vert_lines_right = []
        
        self.ladder_bottom = self.margin_bottom + self.layer_spacing * self.layer_idx
        self.ladder_top = self.margin_bottom + self.layer_spacing * (self.layer_idx+1)

        for multiplier in [-1, 1]:
            line = Line(points=(self.x_center + multiplier*X_BUFFER, self.ladder_bottom, self.x_center + multiplier*X_BUFFER, self.ladder_top), width = 5)
            if multiplier == -1:
                self.vert_lines_left.append(line)
            else:
                self.vert_lines_right.append(line)
            self.add(line)

        center_line_y = self.ladder_bottom  + self.layer_spacing/4
        for _ in range(1, self.num_ladder_rungs+1):
            center_line = Line(points=(self.x_center - X_BUFFER, center_line_y, self.x_center + X_BUFFER, center_line_y), width = 5)
            center_line_y += self.layer_spacing/4
            self.add(center_line)
            self.horiz_lines.append(center_line)

    def get_x_center(self):
        return self.x_center

    def ladder_loc(self):
        return (self.x_center, self.ladder_bottom, self.ladder_top)
    
    def on_resize(self, win_size, margin_side, margin_bottom, layer_spacing):
        self.margin_side = margin_side
        self.margin_bottom = margin_bottom
        self.layer_spacing = layer_spacing
        self.ladder_bottom = self.margin_bottom + self.layer_spacing * self.layer_idx
        self.ladder_top = self.margin_bottom + self.layer_spacing * (self.layer_idx+1)
        self.furthest_x_center_loc = int(win_size[0] - 2*self.margin_side - X_BUFFER - win_size[0]/33.33)
        self.x_center = self.random_number_chosen*(self.furthest_x_center_loc/self.init_furthest_x_center_loc) + self.margin_side + win_size[0]/100
        for line in self.vert_lines_left:
            line.points = (self.x_center + -1*X_BUFFER, self.ladder_bottom, self.x_center + -1*X_BUFFER, self.ladder_top)
        for line in self.vert_lines_right:
            line.points = (self.x_center + X_BUFFER, self.ladder_bottom, self.x_center + X_BUFFER, self.ladder_top)
        for i in range(len(self.horiz_lines)):
            line = self.horiz_lines[i]
            center_line_y = self.ladder_bottom  + (i+1)*self.layer_spacing/4
            line.points = (self.x_center - X_BUFFER, center_line_y, self.x_center + X_BUFFER, center_line_y)

class BackgroundDisplay(Widget):
    def __init__(self):
        super(BackgroundDisplay, self).__init__()
        self.margin_side = Window.width / 10
        self.margin_bottom = Window.height / 10
        self.layer_spacing = Window.height / 8
        self.num_layers = 7
        self.layers = []
        self.x_centers_to_avoid = {idx: set() for idx in range(self.num_layers)}

        for i in range(self.num_layers):
            this_line = Line(points=(self.margin_side, self.margin_bottom + self.layer_spacing * i, Window.width - self.margin_side, self.margin_bottom + self.layer_spacing * i), width = 6)
            self.canvas.add(this_line)
            self.layers.append(this_line)
        

        self.ladders = []
        self.ladder_locs = set() #set of (x, y_bottom, y_top)
        self.generate_ladders()

        self.counter= BirdCounter()
        self.add_widget(self.counter)

        self.remaining_lives = 0
        self.hearts = dict()
        self.heart_base_pos = (Window.width*8/9, Window.height*7/9)

        self.collected_inst = []

    def reset(self):
        self.canvas.clear()
        self.remove_widget(self.counter)
        self.counter= BirdCounter()
        self.ladders = []
        self.x_centers_to_avoid = {idx: set() for idx in range(self.num_layers)}
        self.ladder_locs = set()
        self.hearts = dict()
        self.generate_ladders()
        

    def generate_ladders(self):
        for layer_idx in range(self.num_layers-1):
            for _ in range(2):
                this_ladder = Ladder(self.margin_side, self.margin_bottom, self.layer_spacing, layer_idx, self.x_centers_to_avoid)
                self.canvas.add(this_ladder)
                self.ladders.append(this_ladder)
                self.x_centers_to_avoid[layer_idx].add(this_ladder.get_x_center())
                self.x_centers_to_avoid[layer_idx+1].add(this_ladder.get_x_center())
                self.ladder_locs.add(this_ladder.ladder_loc())

    def add_one_to_count(self):
        self.counter.add_one_to_count()

    def get_margin_side(self):
        return self.margin_side
    
    def get_margin_bottom(self):
        return self.margin_bottom
    
    def get_layer_spacing(self):
        return self.layer_spacing
    
    def get_buffer(self):
        return X_BUFFER

    def can_begin_climbing(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        # TODO - make this take into account the width of ladders once ladder isn't just a line
        can_climb = False
        for loc in self.ladder_ends('B'):
            if abs(pos[0]-loc[0]) < X_BUFFER and abs(pos[1]-loc[1]) < Y_BUFFER:
                can_climb = True
                break
        return can_climb
    
    def can_begin_descending(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        can_descend = False
        for loc in self.ladder_ends('T'):
            if abs(pos[0]-loc[0]) < X_BUFFER and abs(pos[1]-loc[1]) < Y_BUFFER:
                can_descend = True
                break
        return can_descend

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        # TODO - make this take into account the width of ladders once ladder isn't just a line
        can_climb = False
        
        for loc in self.ladder_locs:
            if (abs(pos[0]-loc[0]) < X_BUFFER and pos[1] < loc[2] and pos[1] > loc[1] - Y_EPSILON):
                can_climb = True
                break
        return can_climb
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        can_descend = False
        for loc in self.ladder_locs:
            if (abs(pos[0]-loc[0]) < X_BUFFER and pos[1] - Y_EPSILON < loc[2] and pos[1] > loc[1]):
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

    def add_lives(self, number_lives):
        self.remaining_lives = number_lives
        for life_idx in range(number_lives):
            heart_pos = (self.heart_base_pos[0], self.heart_base_pos[1] - life_idx*Window.height/9)
            heart = Image(source='../data/heart.png', size_hint_x=0.8, anim_delay=1, keep_data=True, pos = heart_pos)
            self.hearts[life_idx] = heart
            self.add_widget(heart)
    
    def add_collected(self, inst_src, idx):
        inst_pos = (self.heart_base_pos[0], Window.height - self.heart_base_pos[1] - (idx-1)*Window.height/9)
        inst_img = Image(source=inst_src, size_hint_x=0.8, anim_delay=1, keep_data=True, pos = inst_pos)
        self.add_widget(inst_img)
    
    def lose_life(self):
        self.remaining_lives -= 1
        self.remove_widget(self.hearts[self.remaining_lives])
        del self.hearts[self.remaining_lives]

    def on_resize(self, win_size):
        global Y_EPSILON, X_BUFFER, Y_BUFFER
        Y_EPSILON = float(win_size[1]/150)
        X_BUFFER = float(win_size[0]/50)
        Y_BUFFER = float(win_size[1]/37.5)

        self.ladder_locs = set()
        self.margin_side = win_size[0] / 10
        self.margin_bottom = win_size[1] / 10
        self.layer_spacing = win_size[1] / 8

        for ladder in self.ladders:
            ladder.on_resize(win_size, self.margin_side, self.margin_bottom, self.layer_spacing)
            self.ladder_locs.add(ladder.ladder_loc())

        for i in range(len(self.layers)):
            layer = self.layers[i]
            layer.points = self.margin_side, self.margin_bottom + self.layer_spacing * i, win_size[0] - self.margin_side, self.margin_bottom + self.layer_spacing * i

    def on_update(self):
        pass #TODO
