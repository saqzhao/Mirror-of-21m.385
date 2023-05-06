from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CRectangle, CLabelRect

font_sz = metrics.dp(20)
button_side = metrics.dp(100)
button_sz = (button_side, button_side)

class PauseButton(Widget):
    def __init__(self, pause_callback):
        super(PauseButton, self).__init__()
        self.pause_button = Button(font_size=font_sz, size = button_sz, background_normal = '../data/pause_button.png', background_down = '../data/pause_button.png', pos = (Window.width*19/20, Window.height/20))
        self.pause_callback = pause_callback
        self.pause_button.bind(on_press = self.pause)
        self.add_widget(self.pause_button)
        self.play_button = Button(font_size=font_sz, size = button_sz, background_normal = '../data/play_button.png', background_down = '../data/play_button.png', pos = (Window.width*19/20, Window.height/20))
        self.play_button.bind(on_press = self.play)
    
    def pause(self, _):
        self.pause_callback()
        self.add_widget(self.play_button)
    
    def play(self, _):
        self.remove_widget(self.play_button)
        self.pause_callback()
