import sys, os, random
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from imslib.gfxutil import CLabelRect
from kivy.core.window import Window
from kivy.uix.image import Image
from BirdCounter import BirdCounter
from ScreenBoundaries import ScreenBoundaries

EPSILON = float(5)
BUFFER = float(20)

class Ladder(InstructionGroup):
    def __init__(self, margin_side, margin_bottom, layer_spacing, layer_idx, x_centers_to_avoid = None):
        super(Ladder, self).__init__()
        self.layer_idx = layer_idx
        self.margin_bottom = margin_bottom
        self.layer_spacing = layer_spacing
        self.num_ladder_rungs = 3
        self.furthest_x_center_loc = Window.width - 2*margin_side - BUFFER - 30
        self.x_center = margin_side + 10 + random.randint(0, self.furthest_x_center_loc)
        if x_centers_to_avoid[self.layer_idx] is not None:
            while any((abs(pos-self.x_center) < 3*BUFFER) for pos in x_centers_to_avoid[self.layer_idx]):
                self.x_center = margin_side + 10 + random.randint(0, self.furthest_x_center_loc)
        
        self.ladder_bottom = self.margin_bottom + self.layer_spacing * self.layer_idx
        self.ladder_top = self.margin_bottom + self.layer_spacing * (self.layer_idx+1)

        for multiplier in [-1, 1]:
            line = Line(points=(self.x_center + multiplier*BUFFER, self.ladder_bottom, self.x_center + multiplier*BUFFER, self.ladder_top), width = 5)
            self.add(line)

        center_line_y = self.ladder_bottom  + self.layer_spacing/4
        for _ in range(1, self.num_ladder_rungs+1):
            center_line = Line(points=(self.x_center - BUFFER, center_line_y, self.x_center + BUFFER, center_line_y), width = 5)
            center_line_y += self.layer_spacing/4
            self.add(center_line)

    def get_x_center(self):
        return self.x_center

    def ladder_loc(self):
        return (self.x_center, self.ladder_bottom, self.ladder_top)

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
        self.add_widget(ScreenBoundaries())

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

    def add_lives(self, number_lives):
        self.remaining_lives = number_lives
        for life_idx in range(number_lives):
            heart_pos = (self.heart_base_pos[0], self.heart_base_pos[1] - life_idx*Window.height/9)
            heart = Image(source='../data/heart.png', size_hint_x=0.8, anim_delay=1, keep_data=True, pos = heart_pos)
            self.hearts[life_idx] = heart
            self.add_widget(heart)
    
    def add_collected(self, inst_src, idx):
        inst_pos = (self.heart_base_pos[0], Window.height - self.heart_base_pos[1] - idx*Window.height/9)
        inst_img = Image(source=inst_src, size_hint_x=0.8, anim_delay=1, keep_data=True, pos = inst_pos)
        self.add_widget(inst_img)
    
    def lose_life(self):
        self.remaining_lives -= 1
        self.remove_widget(self.hearts[self.remaining_lives])
        del self.hearts[self.remaining_lives]

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self):
        pass #TODO
