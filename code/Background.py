import sys, os, random
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from imslib.gfxutil import CLabelRect
from kivy.core.window import Window
from kivy.uix.image import Image
from GameAccessories import BirdCounter

EPSILON = float(5)
BUFFER = float(20)

class Ladder(InstructionGroup):
    def __init__(self, margin_side, margin_bottom, layer_spacing, i, x_centers_to_avoid = None):
        super(Ladder, self).__init__()
        self.i = i
        self.margin_bottom = margin_bottom
        self.layer_spacing = layer_spacing
        self.x_center = margin_side + 10 + random.randint(0, Window.width - 2*margin_side - BUFFER - 30)
        if x_centers_to_avoid is not None:
            while any((abs(pos-self.x_center) < 2*BUFFER) for pos in x_centers_to_avoid):
                self.x_center = margin_side + 10 + random.randint(0, Window.width - 2*margin_side - BUFFER - 30)
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

    def get_x_center(self):
        return self.x_center

    def bounding_box(self):
        return (self.x_center - BUFFER, self.margin_bottom + self.layer_spacing * self.i, self.x_center + BUFFER, self.margin_bottom + self.layer_spacing * (self.i+1))

class BackgroundDisplay(Widget):
    def __init__(self):
        super(BackgroundDisplay, self).__init__()
        print('entering bg')
        self.margin_side = Window.width / 10
        self.margin_bottom = Window.height / 10
        self.layer_spacing = Window.height / 8
        self.layers = []
        self.x_centers_to_avoid = []
        print('BG A')

        for i in range(7):
            this_line = Line(points=(self.margin_side, self.margin_bottom + self.layer_spacing * i, Window.width - self.margin_side, self.margin_bottom + self.layer_spacing * i), width = 6)
            self.canvas.add(this_line)
            self.layers.append(this_line)
        
        print('BG made layers')

        self.ladders = []
        self.ladder_locs = set() #set of (x, y_bottom, y_top)
        for i in range(len(self.layers)-1):
            print('entering ladder ', i)
            for _ in range(2):
                this_ladder = Ladder(self.margin_side, self.margin_bottom, self.layer_spacing, i, self.x_centers_to_avoid)
                self.canvas.add(this_ladder)
                self.ladders.append(this_ladder)
                self.x_centers_to_avoid.append(this_ladder.get_x_center())
                self.ladder_locs.add((0.5*(this_ladder.bounding_box()[0] + this_ladder.bounding_box()[2]), this_ladder.bounding_box()[1], this_ladder.bounding_box()[3]))
            print('ladder ', i)
        print('BG made ladders')
        # TODO: adjust position of counter using some value other than 20
        self.counter= BirdCounter((Window.width*8/9-20, Window.height*8/9))
        self.add_widget(self.counter)
        print('finished setting up background display')

    def add_one_to_count(self):
        print("in add one to count in background.py")
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

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self):
        pass #TODO

class BirdCounter(Widget):
    def __init__(self, pos):
        super(BirdCounter, self).__init__()
        self.count = 0
        self.bird_left = '../data/bird_left.gif'
        self.bird_right = '../data/bird_right.gif'
        self.pos=pos
        self.spacing = int(Window.width/10)
        self.bird = Image(source = self.bird_right, anim_delay=1, keep_data = True, pos = (self.pos))

        #TODO: adjust position of counter
        self.score_display = CLabelRect(cpos=(self.pos[0] + self.spacing, self.pos[1]+ self.spacing/2), text=f'x {self.count}', font_size=21)
        self.add_widget(self.bird)
        self.canvas.add(self.score_display)

    def add_one_to_count(self):
        print("adding one to count in BirdCounter object")
        # WHY TF ISN:T THIS UPDATING ??
        self.count +=1
        self.score_display.text = f'x {self.count}'
        print(f"Score is {self.count}")

    def on_update(self):
        self.score_display.text = f'x {self.count}'
