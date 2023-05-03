import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy import metrics
from imslib.gfxutil import CLabelRect

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(20)
button_width = metrics.dp(200)
button_height = metrics.dp(100)

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "Title Screen\n"
        self.add_widget(self.info)
        self.title = Title()
        self.add_widget(self.title)

        self.start_button = Button(text='Choose Intervals', font_size=font_sz, size = (button_width, button_height), pos = (Window.width/3-button_width/2, Window.height/2-button_height/2))
        self.start_button.bind(on_release= lambda x: self.switch_to('intro'))
        self.add_widget(self.start_button)    

        self.levels_button = Button(text='Choose Level', font_size=font_sz, size = (button_width, button_height), pos = (Window.width*2/3-button_width/2, Window.height/2-button_height/2))
        self.levels_button.bind(on_release= lambda x: self.switch_to('levels'))
        self.add_widget(self.levels_button)    
        

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to_main()

    # if you want on_update() called when a screen is NOT active, then pass in an extra argument:
    # always_update=True to the screen constructor.
    def on_update(self):
        pass

    def on_resize(self, win_size):
        self.start_button.pos = (Window.width/3-button_width/2, Window.height/2-button_height/2)
        self.levels_button.pos = (Window.width*2/3-button_width/2, Window.height/2-button_height/2)
        resize_topleft_label(self.info)
        pass

class Title(Widget):
	def __init__(self):
		super(Title, self).__init__()
		self.title = CLabelRect(cpos=(Window.width/2, Window.height*3/4), text=f'SERENADE FOR TIM', font_size=40)
		self.canvas.add(self.title)
		self.art_credit = CLabelRect(cpos=(Window.width/2, Window.height*1/10), text=f'Wide Tim property of Margaret Zheng', font_size=5)
		self.canvas.add(self.art_credit)