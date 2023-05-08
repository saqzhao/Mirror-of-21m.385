import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CLabelRect, CRectangle, Color
from Help import HelpButton
from HomeButton import HomeButton
from kivy.uix.image import Image

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(20)
button_width = metrics.dp(200)
button_height = metrics.dp(100)

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(always_update=False, **kwargs)

        self.title = Title()
        self.add_widget(self.title)

        self.start_button = Button(text='Choose Intervals', font_size=font_sz, size = (button_width, button_height), pos = (Window.width/3-button_width/2, Window.height/2-button_height/2))
        self.start_button.bind(on_release= lambda x: self.switch_to('intro'))
        self.add_widget(self.start_button)    

        self.levels_button = Button(text='Choose Level', font_size=font_sz, size = (button_width, button_height), pos = (Window.width*2/3-button_width/2, Window.height/2-button_height/2))
        self.levels_button.bind(on_release= lambda x: self.switch_to('levels'))
        self.add_widget(self.levels_button) 

        self.help_button = HelpButton(self)
        self.add_widget(self.help_button)

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to_main()

    def on_resize(self, win_size):
        self.start_button.pos = (Window.width/3-button_width/2, Window.height/2-button_height/2)
        self.levels_button.pos = (Window.width*2/3-button_width/2, Window.height/2-button_height/2)
        self.title.on_resize(win_size)

class Title(Widget):
    def __init__(self):
        super(Title, self).__init__()
        title_image = '../data/title.jpg'        
        size =(Window.width*3/4, Window.height*1/4) # 800,400
        self.title = Image(source = title_image)
        self.title.size = size
        self.title.pos = (Window.width/2- 1/2*size[0], Window.height*3/4-1/2*size[1])
        self.add_widget(self.title)

    def on_resize(self, win_size):
        size = (win_size[0]*3/4, win_size[1]*1/4)
        self.title.size = size
        self.title.pos = (win_size[0]/2- 1/2*size[0], win_size[1]*3/4-1/2*size[1])