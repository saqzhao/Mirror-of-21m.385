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
button_width = metrics.dp(120)
button_height = metrics.dp(100)

class IntroScreen(Screen):
    def __init__(self, start_callback, interval_callback, **kwargs):
        super(IntroScreen, self).__init__(always_update=False, **kwargs)

        self.info = topleft_label()
        self.info.text = "Intro/Settings Screen\n"
        self.info.text += "→: Begin game\n"
        self.start_callback = start_callback
        self.interval_callback = interval_callback
        self.add_widget(self.info)

        self.start_button = Button(text='Begin game', font_size=font_sz, size = (button_width, button_height), pos = (Window.width/2, Window.height/2))
        self.start_button.bind(on_release= lambda x: self.switch_to_main())
        self.add_widget(self.start_button)    

        print('whatsup')
        intervals = ['2m', '2M', '3m', '3M', '4', '5', '6m', '6M', '7m', '7M', '8']
        interval_locs = []
        self.button_centerline_margin = Window.width/20
        print(len(intervals))
        self.button_size = (Window.width/15, Window.height/20)
        self.button_distance = self.button_size[0]*1.3
        interval_locs.append((Window.width/2, Window.height*2/5)) # bottom row middle
        for idx in range(1, 11):
            if idx % 4 == 1: # top row left
                interval_locs.append((Window.width/2+self.button_centerline_margin+1.2*self.button_distance*(idx-1)/4, Window.height*1/5))
            elif idx % 4 == 2: # top row right
                interval_locs.append((Window.width/2-self.button_centerline_margin-1.2*self.button_distance*(idx-2)/4, Window.height*1/5))
            elif idx == 3:
                interval_locs.append((Window.width/2+self.button_centerline_margin+.3*self.button_distance, Window.height*2/5))
            elif idx == 4:
                interval_locs.append((Window.width/2-self.button_centerline_margin-.3*self.button_distance, Window.height*2/5))
            elif idx % 4 == 3: # bottom row left
                interval_locs.append((Window.width/2+self.button_centerline_margin+1.2*self.button_distance*(idx-3)/4, Window.height*2/5))
            elif idx % 4 == 0: # bottom row right
                interval_locs.append((Window.width/2-self.button_centerline_margin-1.2*self.button_distance*(idx-4)/4, Window.height*2/5))
        i = 0
        for loc, opt in zip(interval_locs, intervals):
            i += 1
            button = IntervalButton(opt, loc, self.button_size, self.interval_callback)
            self.add_widget(button)

    def switch_to_main(self):
        self.switch_to('main')
        self.start_callback()

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'right':
            self.switch_to_main()

    # if you want on_update() called when a screen is NOT active, then pass in an extra argument:
    # always_update=True to the screen constructor.
    def on_update(self):
        self.info.text = "Intro/Settings Screen\n"
        self.info.text += "→: Begin game\n"

    def on_resize(self, win_size):
        self.start_button.pos = (Window.width/2, Window.height/2)
        resize_topleft_label(self.info)

class IntervalButton(Widget):
    def __init__(self, buttonLabel, pos, button_size, callback):
        super(IntervalButton, self).__init__()
        self.buttonLabel = buttonLabel
        print('label', self.buttonLabel)
        print('pos', pos)
        btn = Button(text = self.buttonLabel,
                     font_size = "20sp",
                     background_color = (1, 1, 1, 1),
                     color = (1, 1, 1, 1),
                     size = button_size,
                     size_hint = (0.2, 0.2),
                     pos = pos)
        self.callback = callback
        btn.bind(on_press = self.add_interval)
        self.add_widget(btn)

    def add_interval(self, _):
        self.callback(self.buttonLabel)