import sys, os, random
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line
from imslib.gfxutil import CLabelRect
from kivy.core.window import Window
from kivy.uix.image import Image

class BirdCounter(Widget):
    def __init__(self):
        super(BirdCounter, self).__init__()
        self.count = 0
        self.bird_left = '../data/bird_left.gif'
        self.bird_right = '../data/bird_right.gif'
        self.spacing = int(Window.width/10)
        self.pos = (Window.width/2, Window.height/90)
        self.bird = Image(source = self.bird_right, anim_delay=1, keep_data = True, pos = self.pos)

        #TODO: adjust position of counter
        self.score_display = CLabelRect(cpos=(self.pos[0] + self.spacing, self.pos[1]+ self.spacing/2), text=f'x {self.count}', font_size=21)
        self.add_widget(self.bird)
        self.canvas.add(self.score_display)

    def add_one_to_count(self):
        self.count +=1
        self.score_display.set_text(f'x {self.count}')

    def on_update(self):
        # self.score_display.text = f'x {self.count}'
        pass
    
