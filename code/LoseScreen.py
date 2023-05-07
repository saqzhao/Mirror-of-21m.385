import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from imslib.gfxutil import CRectangle, CLabelRect

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy import metrics
from kivy.uix.image import Image
from kivy.graphics import Color


from Help import HelpButton
from HomeButton import HomeButton

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(15)
button_width = metrics.dp(100)
button_height = metrics.dp(100)

class LoseScreen(Screen):
    def __init__(self, **kwargs):
        # interval callback: str -> adding interval to list
        super(LoseScreen, self).__init__(always_update=False, **kwargs)
        
        self.help_button = HelpButton(self)
        self.add_widget(self.help_button)

        self.home_button = HomeButton(self)
        self.add_widget(self.home_button)

        self.daze_character = Image(source='../data/daze.png', anim_delay=1, keep_data=True, pos = (Window.width/4, Window.height/2))
        self.add_widget(self.daze_character)
        
        self.text = '''Oh no! You've run into too many birds, and became lost on 
                            your way to Wide Tim. Better luck next time!'''
        self.canvas.add(Color(1 ,1, 1, 1))
        self.label = CLabelRect(cpos=(Window.width*3/4, Window.height/2), text=self.lose_text, font_size=font_sz)
        self.canvas.add(self.instructions)
        