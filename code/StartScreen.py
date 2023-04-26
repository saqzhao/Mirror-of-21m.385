import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy import metrics

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(20)
button_sz = metrics.dp(100)

class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super(IntroScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "Intro/Settings Screen\n"
        self.info.text += "→: Begin game\n"
        self.add_widget(self.info)

        self.button = Button(text='Begin game', font_size=font_sz, size = (button_sz, button_sz), pos = (Window.width/2, Window.height/2))
        self.button.bind(on_release= lambda x: self.switch_to('main'))
        self.add_widget(self.button)

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to('main')

    # if you want on_update() called when a screen is NOT active, then pass in an extra argument:
    # always_update=True to the screen constructor.
    def on_update(self):
        self.info.text = "Intro/Settings Screen\n"
        self.info.text += "→: Begin game\n"

    def on_resize(self, win_size):
        self.button.pos = (Window.width/2, Window.height/2)
        resize_topleft_label(self.info)