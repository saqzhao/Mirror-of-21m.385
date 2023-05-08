import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label, CLabelRect

from imslib.screen import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics
from kivy.uix.image import Image
from kivy.graphics import Color

from HomeButton import HomeButton


font_sz = metrics.dp(20)
button_sz = metrics.dp(325)
MARGIN = 10

class GameOverScreen(Screen):
    def __init__(self, main_screen, **kwargs):
        super(GameOverScreen, self).__init__(always_update=True, **kwargs)
        self.main_screen = main_screen

        self.button_continue = Button(text = "Continue Game with Same Settings", font_size = font_sz,  size = (button_sz, button_sz/3), pos = (Window.width/10 - MARGIN, Window.height/2))
        self.button_continue.bind(on_release = lambda x: self.switch_to('main'))
        self.add_widget(self.button_continue)

        self.button_back = Button(text = "Go Back to Settings", font_size = font_sz,  size = (button_sz, button_sz/3), pos = (Window.width*5/10 + MARGIN, Window.height/2))
        self.button_back.bind(on_release = lambda x: self.switch_to('intro'))
        self.add_widget(self.button_back)

        self.home_button = HomeButton(self)
        self.add_widget(self.home_button)

        self.daze_character = Image(source='../data/daze.png', anim_delay=1, keep_data=True, pos = (Window.width/4, Window.height*14/20), width=200, height=200)
        self.add_widget(self.daze_character)
        
        self.game_over_text = '''Oh no! You've run into too many birds, 
                                 \nand got lost on your way to Wide Tim. 
                                 \nBetter luck next time!'''
        self.canvas.add(Color(1 ,1, 1, 1))
        self.instructions = CLabelRect(cpos=(Window.width*3/4, Window.height*16/20), text=self.game_over_text, font_size=font_sz*.5)
        self.canvas.add(self.instructions)

    def on_enter(self):
        pass

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to('intro')

    def on_resize(self, win_size):
        width = win_size[0]
        height = win_size[1]
        self.button_continue.pos = (width/10 - MARGIN, height/2)
        self.button_back.pos = (width*5/10 + MARGIN, height/2)
        self.home_button.on_resize(win_size)
        self.daze_character.pos = (width/4, height*14/20)
        self.instructions.cpos =(width*3/4, height*16/20)
