import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy import metrics

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(20)
button_width = metrics.dp(100)
button_height = metrics.dp(100)

class LevelSelectScreen(Screen):
    def __init__(self, start_callback, interval_callback, **kwargs):

        # interval callback: str -> adding interval to list
        super(LevelSelectScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "Level Select Screen\n"
        self.start_callback = start_callback
        self.interval_callback = interval_callback
        self.add_widget(self.info)


        # TODO: Decide where on screen home button goes
        home_image = '../data/home_image.png'
        self.home_button = Button(text='', font_size=font_sz, background_normal =home_image, pos = (Window.width*1/9, Window.height*9/10))
        self.home_button.bind(on_release= lambda x: self.switch_to('title'))
        self.add_widget(self.home_button)    

        self.start_button = Button(text='Begin game', font_size=font_sz, size = (button_width, button_height), pos = (Window.width/2, Window.height/2))
        self.start_button.bind(on_release= lambda x: self.start_game())
        self.add_widget(self.start_button)    


        self.level_selected = None
        # intervals = ['2m', '2M', '3m', '3M', '4', '5', '6m', '6M', '7m', '7M', '8']

        #These can be changed however

        # Basic gives you two options (?)
        levels_b = [['2M', '8'], ['5', '2m'], ['6M', '3M'], ['2m', '2M'], ['3m', '3M']]
        levels_b_combined = ['2m', '2M', '3m', '3M', '5', '6M', '8']

        # Medium gives you three options (?)
        levels_m = [['2M', '5', '8'], ['3m', '6m', '7M']]
        levels_m_combined = ['2M', '5', '8', '3m', '6m', '7M']

        # Advanced gives you four options (?)
        levels_a = [['2m, 3M, 4, 5']]

        all_levels = []

        # self.all_buttons = {}
        button_size = (button_width, button_height)
        basic_height = Window.height*2/5
        basic_width_spacing = Window.width/(len(levels_b)+1)
        for i in range(len(levels_b)):
            level = levels_b[i] # List of Intervals (strings)
            all_levels.append(level)
             # level_name, button_intervals, pos, button_size, callback
            button = LevelButton(i, level, (basic_width_spacing*i, basic_height), button_size, self.select_this_level_callback)
            # self.all_buttons[i] = button
            self.add_widget(button)


        


    def start_game(self):
        if self.level_selected == None:
            return
        level_intervals = self.level_selected.button_intervals
        for interval in level_intervals:
            self.interval_callback(interval)
        self.switch_to('main')
        self.start_callback()

    def select_this_level_callback(self, button):
        if self.level_selected!=None:
            self.level_selected.another_pressed()
        self.level_selected = button

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to_main()

    # if you want on_update() called when a screen is NOT active, then pass in an extra argument:
    # always_update=True to the screen constructor.
    def on_update(self):
        self.info.text = "Level Select Screen\n"


    def on_resize(self, win_size):
        self.start_button.pos = (Window.width/2, Window.height/2)
        resize_topleft_label(self.info)

class LevelButton(Widget):
    def __init__(self, level_name, button_intervals, pos, button_size, callback):
        super(LevelButton, self).__init__()
        self.level_name = level_name
        self.button_intervals=button_intervals
        button_label = "Level {level_name}:\n"
        button_label += ",".join(button_intervals)
        self.btn = Button(text = button_label,
                     font_size = "20sp",
                     background_color = (1, 1, 1, 1),
                     color = (1, 1, 1, 1),
                     size = button_size,
                     size_hint = (0.2, 0.2),
                     pos = pos)
        self.callback = callback
        self.btn.bind(on_press = self.pressed_button_action)
        self.add_widget(self.btn)
        self.pressed = False

    def pressed_button_action(self, _):
        self.pressed = True
        self.btn.background_color= (.5,.5,.5,.5)
        self.callback(self)

    def another_pressed(self):
        self.pressed = False
        self.btn.background_color= (1, 1, 1, 1)