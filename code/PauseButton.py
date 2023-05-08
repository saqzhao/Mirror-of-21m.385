from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CRectangle, CLabelRect
from HomeButton import HomeButton

font_sz = metrics.dp(20)
button_side = metrics.dp(100)
button_sz = (button_side, button_side)

class PauseButton(Widget):
    def __init__(self, pause_callback, screen):
        super(PauseButton, self).__init__()
        self.paused = False
        self.pause_button = Button(size = button_sz, background_normal = '../data/pause_button.png', pos = (Window.width*8/9,  Window.height/90))
        self.pause_callback = pause_callback
        self.pause_button.bind(on_press = self.pause)
        self.background = CRectangle(cpos=(Window.width/2, Window.height/2), csize=(Window.width, Window.height))
        self.add_widget(self.pause_button)
        self.home_button = HomeButton(screen)
        self.play_button = Button(size = button_sz, background_normal = '../data/play_button.png', pos = (Window.width*8/9,  Window.height/90))
        self.play_button.bind(on_press = self.play)
        print('pause button init: ', self.paused)
    
    def pause(self, _):
        self.paused = True
        self.pause_callback()
        self.remove_widget(self.pause_button)
        self.canvas.add(Color(0.5, 0.5, 0.5, .75))
        self.canvas.add(self.background)
        self.add_widget(self.play_button)
        self.add_widget(self.home_button)
    
    def play(self, _):
        self.paused = False
        self.canvas.clear()
        self.remove_widget(self.play_button)
        self.remove_widget(self.home_button)
        self.add_widget(self.pause_button)
        self.pause_callback()

    def toggle(self):
        print('self.paused before: ', self.paused)
        if not self.paused:
            self.pause(True)
        else:
            self.play(True)
        print('self.paused after: ', self.paused)
