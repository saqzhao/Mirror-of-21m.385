from kivy.graphics.instructions import InstructionGroup
from imslib.gfxutil import CEllipse
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import random

NUM_LAYERS = 7
BUFFER = 20

class CollectedInstrumentDisplay(Widget):
    def __init__(self, background, character, instrument, layer, collect_callback, x_centers_to_avoid = None):
        super(CollectedInstrumentDisplay, self).__init__()
        self.layer = layer
        self.instrument_text = instrument
        self.instrument_source = '../data/' + instrument + '_2.gif'
        self.background = background
        self.character = character
        self.margin_side = self.background.get_margin_side()
        self.margin_bottom = self.background.get_margin_bottom()
        self.layer_spacing = self.background.get_layer_spacing()
        self.buffer = self.background.get_buffer()
        self.x_center = self.margin_side + 10 + random.randint(0, Window.width - self.margin_side - 2*BUFFER)
        if x_centers_to_avoid is not None:
            while any((abs(pos-self.x_center) < 2*BUFFER) for pos in x_centers_to_avoid):
                self.x_center = self.margin_side + 10 + random.randint(0, Window.width - self.margin_side - 2*BUFFER)
        self.y_center = ((self.margin_bottom + self.layer_spacing * self.layer) + (self.margin_bottom + self.layer_spacing * (self.layer+1)))/2
        self.radius = Window.width/20

        self.instrument = Image(source = self.instrument_source, anim_delay=0, keep_data = True)
        self.instrument.pos[0] = self.x_center-self.radius
        self.instrument.pos[1] = self.y_center-self.radius
        self.add_widget(self.instrument)
        self.background.add_widget(self)
        self.collect_callback = collect_callback
        self.active = True
        
    def on_resize(self, win_size):
        pass #TODO

    def on_update(self, dt):
        if self.active:
            character_pos = self.character.to_screen_pos()
            if ((abs(character_pos[0]-self.x_center)**2 + abs(character_pos[1]-self.y_center)**2)**0.5 < 50):
                self.collect_callback(self)
                self.remove_widget(self.instrument)
                self.active = False

    def get_inst_source(self):
        return self.instrument_source

    def get_instrument(self):
        return self.instrument_text
    
    def get_x_pos(self):
        return self.x_center