import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "EndScreen\n"
        self.add_widget(self.info)

    def on_resize(self, win_size):
        resize_topleft_label(self.info)