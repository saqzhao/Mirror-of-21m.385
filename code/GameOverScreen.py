import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label, CLabelRect

from imslib.screen import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

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

        self.title = CLabelRect(cpos=(Window.width/2, Window.height*16/20), text=f'Game Over :(', font_size=30)
        self.canvas.add(self.title)
        self.instruction_text = '''Oh no! You missed too many interval quizzes carried by birds, and got lost on the 
                                \npath to Wide Tim. Better luck next time! We encourage you to keep practicing.'''
        self.instructions = CLabelRect(cpos=(Window.width/2, Window.height*7/20), text=self.instruction_text, font_size=15)
        self.canvas.add(self.instructions)

    def on_enter(self):
        self.main_screen.final_song_audio_ctrl.play_serenade()

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to('intro')

    def on_resize(self, win_size):
        # resize_topleft_label(self.info)
        pass