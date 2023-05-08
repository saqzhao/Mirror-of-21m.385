import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label
from imslib.screen import Screen

from kivy.core.window import Window
from kivy import metrics
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from HomeButton import HomeButton
from Help import HelpButton

# metrics allows kivy to create screen-density-independent sizes.
# Here, 20 dp will always be the same physical size on screen regardless of resolution or OS.
# Another option is to use metrics.pt or metrics.sp. See https://kivy.org/doc/stable/api-kivy.metrics.html
font_sz = metrics.dp(20)
button_width = metrics.dp(120)
button_height = metrics.dp(100)

class IntroScreen(Screen):
    def __init__(self, interval_callback, **kwargs):

        # interval callback: str -> adding interval to list
        super(IntroScreen, self).__init__(always_update=False, **kwargs)

        # self.info = topleft_label()
        # self.info.text = "Intro/Settings Screen\n"
        # self.info.text += "→: Begin Game\n"
        # self.start_callback = start_callback
        self.interval_callback = interval_callback
        # self.add_widget(self.info)

        self.home_button = HomeButton(self)
        self.add_widget(self.home_button)    

        start_button_position = (Window.width/2- button_width/2, Window.height*3/5- button_height/2)
        self.start_button = Button(text='Begin Game', font_size=font_sz, size = (button_width, button_height), pos = start_button_position)
        self.start_button.bind(on_release= lambda x: self.switch_to_main())
        self.add_widget(self.start_button)    

        self.intervals = ['2m', '2M', '3m', '3M', '4', '5', '6m', '6M', '7m', '7M', '8']
        self.interval_locs = []
        self.buttons = []

        button_centerline_margin = Window.width/20
        button_size = (Window.width/15, Window.height/20)
        button_spacing = button_size[0]*0.3
        button_distance = button_size[0]*1.3

        height_top = Window.height*2/5
        height_bottom = Window.height* 1/5
        num_top =len(self.intervals)//2
        num_bottom =len(self.intervals)-num_top
        border_o = (Window.width - (num_top)*button_distance)/2
        border_e = (Window.width - num_bottom*button_distance)/2
        
        for idx in range(num_top): # 11 Intervals split 5 then 6
            x = border_o + button_distance*idx
            self.interval_locs.append((x, height_top))

        for idx in range(num_bottom): 
            x = border_e + button_distance*idx
            self.interval_locs.append((x, height_bottom))

        for loc, opt in zip(self.interval_locs, self.intervals):
            button = IntervalButton(opt, loc, button_size, self.interval_callback)
            self.buttons.append(button)
            self.add_widget(button)
        
        self.help_button = HelpButton(self)
        self.add_widget(self.help_button)

    def switch_to_main(self):
        self.switch_to('main')
        # self.start_callback()

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to_main()

    # if you want on_update() called when a screen is NOT active, then pass in an extra argument:
    # always_update=True to the screen constructor.
    def on_update(self):

        pass

    def on_resize(self, win_size):
        self.home_button.on_resize(win_size)
        self.help_button.on_resize(win_size)
        start_button_position = (win_size[0]/2- button_width/2, win_size[1]*3/5- button_height/2)
        self.start_button.pos = start_button_position

        button_centerline_margin = win_size[0]/20
        button_size = (win_size[0]/15, win_size[1]/20)
        button_spacing = button_size[0]*0.3
        button_distance = button_size[0]*1.3

        height_top = win_size[1]*2/5
        height_bottom = win_size[1]* 1/5
        num_top =len(self.intervals)//2
        num_bottom =len(self.intervals)-num_top
        border_o = (Window.width - (num_top)*button_distance)/2
        border_e = (Window.width - num_bottom*button_distance)/2

        self.interval_locs = []
        for idx in range(num_top): # 11 self.Intervals split 5 then 6
            x = border_o + button_distance*idx
            self.interval_locs.append((x, height_top))
        for idx in range(num_bottom): 
            x = border_e + button_distance*idx
            self.interval_locs.append((x, height_bottom))

        for button, loc in zip(self.buttons, self.interval_locs):
            button.set_pos(loc)        

class IntervalButton(Widget):
    def __init__(self, buttonLabel, pos, button_size, interval_callback):
        super(IntervalButton, self).__init__()
        self.buttonLabel = buttonLabel
        self.down = False
        self.btn = Button(text = self.buttonLabel,
                     font_size = "20sp",
                     background_color = (1, 1, 1, 1),
                     color = (1, 1, 1, 1),
                     size = button_size,
                     size_hint = (0.2, 0.2),
                     pos = pos)
        self.interval_callback = interval_callback
        self.btn.bind(on_press = self.pressed_button_action)
        self.add_widget(self.btn)

    def pressed_button_action(self, _):
        if self.down:
            self.remove_interval(_)
        else:
            self.add_interval( _)

    def add_interval(self, _):
        self.down = True
        self.btn.background_color = (.5,.5,.5,.5)
        self.interval_callback(self.buttonLabel)

    def remove_interval(self, _):
        self.down = False
        self.btn.background_color = (1,1,1,1)
        self.interval_callback(self.buttonLabel, False)

    def set_pos(self, pos):
        self.btn.pos = pos