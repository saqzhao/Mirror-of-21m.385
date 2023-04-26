import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

font_sz = metrics.dp(20)
button_sz = metrics.dp(100)

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "EndScreen\n"
        self.add_widget(self.info)
        self.button = Button(text='Restart game', font_size=font_sz, size = (button_sz, button_sz), pos = (Window.width/2, Window.height/2))
        self.button.bind(on_release= lambda x: self.switch_to('intro'))
        self.add_widget(self.button)

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to('intro')

    def on_resize(self, win_size):
        resize_topleft_label(self.info)