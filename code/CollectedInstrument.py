from kivy.graphics.instructions import InstructionGroup
from imslib.gfxutil import CEllipse
from kivy.graphics import Color
from kivy.core.window import Window
import random

NUM_LAYERS = 7
BUFFER = 20

class CollectedInstrumentDisplay(InstructionGroup):
    def __init__(self, background, character, instrument, i, callback, x_centers_to_avoid = None):
        super(CollectedInstrumentDisplay, self).__init__()
        self.background = background
        self.instrument = instrument
        self.character = character
        self.margin_side = self.background.get_margin_side()
        self.margin_bottom = self.background.get_margin_bottom()
        self.layer_spacing = self.background.get_layer_spacing()
        self.buffer = self.background.get_buffer()
        self.x_center = self.margin_side + 10 + random.randint(0, Window.width - self.margin_side - 2*BUFFER)
        if x_centers_to_avoid is not None:
            while any((abs(pos-self.x_center) < 2*BUFFER) for pos in x_centers_to_avoid):
                self.x_center = self.margin_side + 10 + random.randint(0, Window.width - self.margin_side - 2*BUFFER)
        self.y_center = ((self.margin_bottom + self.layer_spacing * i) + (self.margin_bottom + self.layer_spacing * (i+1)))/2
        self.radius = Window.width/20
        self.ellipse = CEllipse(cpos = (self.x_center, self.y_center), csize = (self.radius, self.radius))
        # self.color = Color(rgb = (.7,.7,.7))
        self.color = Color(rgb = (1, 0, 0, 1)) # to distinguish from gray birds
        self.add(self.color)
        self.add(self.ellipse)
        self.background.add(self)
        self.callback = callback
        self.active = True
        
    def on_resize(self, win_size):
        pass #TODO

    def on_update(self, dt):
        if self.active:
            character_pos = self.character.to_screen_pos()
            if ((abs(character_pos[0]-self.x_center)**2 + abs(character_pos[1]-self.y_center)**2)**0.5 < 50):
                self.callback(self)
                self.remove(self.ellipse)
                self.active = False

    def get_instrument(self):
        return self.instrument
    
    def get_x_pos(self):
        return self.x_center