import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle, KFAnim

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Texture
from kivy.core.window import Window
from kivy.core.image import Image
from math import random, randint

class IntervalQuiz(InstructionGroup):
    def __init__(self, mode, options):
        super(IntervalQuiz, self).__init__()
        self.mode = mode
        # self.options = options
        self.options = [2, 3, 5, 8]
        self.midi_options = [2, 4, 7, 12]
        self.timer_bar = CRectangle(cpos=(Window.width/2, Window.height/8), csize = (Window.width/3, Window.height/30))
        self.timer_runout = KFAnim((0, Window.width/3, Window.height/30), (6, 0, Window.height/30))
        self.time = 0
        self.easy_button_locations = {'a': (Window.width/4, Window.height*3/5), 'b': (Window.width*3/4, Window.height*3/5), 
                                      'c': (Window.width/4, Window.height*2/5), 'd': (Window.width/4, Window.height*2/5)}
        self.buttons = []
        self.button_labels = []
        self.button_intervals = []
        self.button_locations = []
        self.button_dimensions = (Window.width/6, Window.height/20)
        pass #TODO

    def button(self, loc, option):
        button  = CRectangle(cpos=loc)
        label = CLabelRect(cpos = loc, text='')
        self.buttons.add(button)
        self.add(button)

    def generate_quiz(self):
        if self.mode == 'easy':
            options = {}
            if len(self.options > 4):
                while len(options) < 4:
                    idx_to_add = randint(0, len(self.options)-1)
                    if idx_to_add not in options:
                        options.add(self.options[idx_to_add])
            else:
                options = self.options
            for loc in zip(self.easy_button_locations, list(options)):
                self.button(loc, )
        else:
            for loc in self.hard_button_locations:
                self.button(loc)

    def on_touch_down(self, touch):
        if self.mode == 'easy':
            for loc in self.easy_button_locations:

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self, time):
        self.time += time
        self.timer_bar.csize = self.timer_runout.eval(self.time)
        if self.time > 6:
            return False
