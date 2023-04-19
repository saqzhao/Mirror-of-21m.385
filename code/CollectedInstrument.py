from kivy.graphics.instructions import InstructionGroup
from imslib.gfxutil import CEllipse
from kivy.graphics import Color
from kivy.core.window import Window
import random

NUM_LAYERS = 7
BUFFER = 20

class CollectedInstrumentDisplay(InstructionGroup):
    def __init__(self, background, i, callback):
        super(CollectedInstrumentDisplay, self).__init__()
        self.background = background
        self.margin_side = self.background.get_margin_side()
        self.margin_bottom = self.background.get_margin_bottom()
        self.layer_spacing = self.background.get_layer_spacing()
        self.buffer = self.background.get_buffer()
        self.x_center = self.margin_side + random.randint(0, Window.width - self.margin_side - BUFFER)
        self.y_center = ((self.margin_bottom + self.layer_spacing * i) + (self.margin_bottom + self.layer_spacing * (i+1)))/2
        self.radius = Window.width/20
        self.ellipse = CEllipse(cpos = (self.x_center, self.y_center), csize = (self.radius, self.radius))
        # self.color = Color(rgb = (.7,.7,.7))
        self.color = Color(rgb = (1, 0, 0, 1)) # to distinguish from gray birds
        self.add(self.color)
        self.add(self.ellipse)
        self.background.add(self)
        self.callback = callback
        
    def on_resize(self, win_size):
        pass #TODO

    def add_instrument(self, instrument):
        self.callback(instrument)
