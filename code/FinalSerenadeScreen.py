import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

from HomeButton import HomeButton

font_sz = metrics.dp(20)
button_sz = metrics.dp(325)
MARGIN = 10

class EndScreen(Screen):
    def __init__(self, main_screen, **kwargs):
        super(EndScreen, self).__init__(always_update=True, **kwargs)
        self.main_screen = main_screen

        self.button_continue = Button(text = "Continue Game with Same Settings", font_size = font_sz,  size = (button_sz, button_sz/3), pos = (Window.width/10 - MARGIN, Window.height/2))
        self.button_continue.bind(on_release = lambda x: self.switch_to('main'))
        self.add_widget(self.button_continue)

        self.button_back = Button(text = "Go Back to Settings", font_size = font_sz,  size = (button_sz, button_sz/3), pos = (Window.width*5/10 + MARGIN, Window.height/2))
        self.button_back.bind(on_release = lambda x: self.switch_to('intro'))
        self.add_widget(self.button_back)

        self.home_button = HomeButton(self)
        self.add_widget(self.home_button)

    def on_enter(self):
        self.main_screen.final_song_audio_ctrl.play_serenade()

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to('intro')

    def on_resize(self, win_size):
        width = win_size[0]
        height = win_size[1]
        self.button_continue.pos = (width/10 - MARGIN, height/2)
        self.button_back.pos = (width*5/10 + MARGIN, height/2)
        self.home_button.on_resize(win_size)
