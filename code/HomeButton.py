import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CRectangle, CLabelRect

font_sz = metrics.dp(20)
button_side = metrics.dp(100)
button_sz = (button_side, button_side)

class HomeButton(Widget):
    def __init__(self, screen):
        super(HomeButton, self).__init__()
        self.home_button = Button(size = button_sz, background_normal='../data/home_image.png', pos = (Window.width/50, Window.height*15/18))
        self.home_button.bind(on_release= lambda x: screen.switch_to('title'))
        self.add_widget(self.home_button)