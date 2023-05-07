import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CRectangle, CLabelRect
import webbrowser

from HomeButton import HomeButton

font_sz = metrics.dp(20)
button_side = metrics.dp(100)
half_button_side = metrics.dp(70)
button_sz = (button_side, button_side)

class HelpButton(Widget):
    def __init__(self, screen, toggle = None, ):
        super(HelpButton, self).__init__()
        self.help_button = Button(text='?', font_size=font_sz*1.3, size = button_sz, background_normal = '../data/circle_button.png', background_down = '../data/circle_button.png', pos = (Window.width/50, Window.height/90))
        self.screen = screen
        self.toggle = toggle
        self.help_button.bind(on_press = self.open_help_screen)
        self.add_widget(self.help_button)
        self.help_widget = HelpScreen(self.remove_help_screen, self.screen)

    def open_help_screen(self, _):
        self.add_widget(self.help_widget)
        if self.toggle != None:
            self.toggle()
    
    def remove_help_screen(self, _):
        self.remove_widget(self.help_widget)
        if self.toggle != None:
            self.toggle()

    def on_resize(self, win_size):
        pos = (win_size[0]/50, win_size[1]/90)
        self.help_button.pos = pos
    
    
class HelpScreen(Widget):
    def __init__(self, exit_screen, screen):
        super(HelpScreen, self).__init__()
        self.remove_help_screen = exit_screen
        self.screen = screen

        # widget background
        self.canvas.add(Color(0.5, 0.5, 0.5, .75))
        self.canvas.add(CRectangle(cpos=(Window.width/2, Window.height/2), csize=(Window.width, Window.height)))
        self.canvas.add(Color(0.5, 0.5, 0.5, 1))
        self.canvas.add(CRectangle(cpos=(Window.width/2, Window.height/2), csize=(Window.width*3/4, Window.height*3/4)))
        self.text_color = Color(1, 1, 1, .8)
        self.canvas.add(self.text_color)
        self.title = CLabelRect(cpos=(Window.width/2, Window.height*16/20), text=f'Instructions', font_size=30)
        self.canvas.add(self.title)
        self.instruction_text = '''Wide Tim is waiting for you to serenade him! To reach Wide Tim and put on 
                                    \nyour best show traverse through the different floors and try not to crash 
                                    \ninto the birds. If you run into a bird, a quiz will be triggered to test 
                                    \nyour interval identification skills. You can also collect instruments to 
                                    \nadd to your performance for Tim!
                                    \n\nTo select what intervals you would like to be quizzed on, navigate to 
                                    \nInterval Select. If you would like to follow a systematic plan to learn 
                                    \nyour intervals, navigate to Level Select.'''
        self.instructions = CLabelRect(cpos=(Window.width/2, Window.height*9/20), text=self.instruction_text, font_size=15)
        self.canvas.add(self.instructions)
        
        self.buttons = set()
        # what are intervals
        self.what_are_intervals = 'https://en.wikipedia.org/wiki/Interval_(music)'
        self.interval_button = Button(text='What are intervals?', font_size=metrics.dp(17), size=(400, 75), pos = (Window.width/2-200, Window.height*26.5/30))
        self.interval_button.bind(on_press = self.open_interval_link)
        self.add_widget(self.interval_button)
        self.buttons.add(self.interval_button)

        # exit button
        button_sz = (1.5*button_side, 1.5*button_side)
        self.exit_button = Button(text='X', font_size=font_sz, size=(.7*button_side, .7*button_side), background_normal = '../data/red_circle_button.png', 
                                  background_down = '../data/red_circle_button.png', pos=(Window.width*50/60, Window.height*49/60))
        self.exit_button.bind(on_press = self.remove_help_screen)
        self.add_widget(self.exit_button)
        self.buttons.add(self.exit_button)

        self.home_button = HomeButton(self.screen)
        self.add_widget(self.home_button)

    def open_interval_link(self, _):
        webbrowser.open(self.what_are_intervals, new=0, autoraise=True)
    
