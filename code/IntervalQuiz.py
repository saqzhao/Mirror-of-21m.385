import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle, KFAnim

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Texture
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.app import App
from kivy.uix.button import Button
from math import random, randint

class QuizButton(App):
    def __init__(self, buttonLabel, pos, is_correct, size, callback):
        btn = Button(text = buttonLabel,
                     font_size = "20sp",
                     background_color = (1, 1, 1, 1),
                     color = (1, 1, 1, 1),
                     background_down = (.5, .5, .5, 1),
                     background_normal = (1, 1, 1, 1),
                     size = size,
                     size_hint = (0.2, 0.2),
                     pos = pos)
        self.is_correct = is_correct
        self.callback = callback
        btn.bind(on_press = self.give_result)
    

    def give_result(self):
        # does something to button if wrong then grays out option
        if not self.is_correct:
            print('wrong')
            # pass
        else: #does something to button if correct
            print('correct')
            pass
        self.callback(self.is_correct)

class IntervalQuiz(InstructionGroup):
    def __init__(self, mode, options, increment_score, generate_interval):
        super(IntervalQuiz, self).__init__()
        self.mode = mode
        self.options = options
        self.timer_bar = CRectangle(cpos=(Window.width/2, Window.height/8), csize = (Window.width/3, Window.height/30))
        self.timer_runout = KFAnim((0, Window.width/3, Window.height/30), (6, 0, Window.height/30))
        self.score = increment_score
        self.interval_audio = generate_interval
        self.fail = False
        self.succeed = False
        self.time = 0
        self.correct_answer = None

        # quiz buttons
        self.button_size = (Window.width/15, Window.height/20)
        self.button_centerline_margin = Window.width/20

        self.button_locations[0] = (Window.width/2, Window.height*3/5) # bottom row middle
        for idx in range(1, 12):
            if idx % 4 == 1: # top row left
                self.button_locations[idx] = (Window.width/2+self.button_centerline_margin+self.button_size*(idx-1)/4, Window.height*2/5)
            elif idx % 4 == 2: # top row right
                self.button_locations[idx] = (Window.width/2+self.button_centerline_margin-self.button_size*(idx-2)/4, Window.height*2/5)
            elif idx % 4 == 3: # bottom row left
                self.button_locations[idx] = (Window.width/2+self.button_centerline_margin+self.button_size*(idx-3)/4, Window.height*3/5)
            elif idx % 4 == 0: # bottom row right
                self.button_locations[idx] = (Window.width/2+self.button_centerline_margin-self.button_size*(idx-4)/4, Window.height*3/5)

        self.buttons = []
        self.button_labels = []

    def generate_quiz_options(self, num_options):
        options = {}
        if len(self.options > num_options):
            while (len(options) < num_options):
                idx_to_add = randint(0, len(self.options)-1)
                if idx_to_add not in options:
                    options.add(self.options[idx_to_add])
        correct = random.choice(options)
        return correct, options

    def quiz_result(self, is_correct):
        if is_correct:
            self.succeed = True
        if not self.fail and is_correct:
            self.score(is_correct)

    def create_buttons(self, locations, options, correct_answer):
        for loc, opt in zip(locations, options):
                is_correct = False if opt != correct_answer else True
                button = QuizButton(opt, loc, is_correct, self.button_size, self.quiz_result)
                # self.buttons.append(button)
                self.add_widget(button)

    def generate_quiz(self):
        if self.mode == 'easy':
            self.correct_answer, all_options = self.generate_quiz_options(4)
            self.interval_audio(self.correct_answer)
            all_options = list(all_options)
            num_options = len(all_options)
            easy_button_locations = [self.button_locations[idx] for idx in range(num_options)]
            self.create_buttons(easy_button_locations, all_options, self.correct_answer)
                
        else:
            self.correct_answer = random.choice(self.options)
            self.interval_audio(self.correct_answer)
            hard_button_locations = [self.button_locations[idx] for idx in range(len(self.options))]
            self.create_buttons(hard_button_locations, self.options, self.correct_answer)

    # def on_touch_down(self, touch):
    #     if self.mode == 'easy':
    #         for loc in self.easy_button_locations:
    #             pass

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self, time):
        self.time += time
        self.timer_bar.csize = self.timer_runout.eval(self.time)
        if self.time > 3 and self.time < 3.3:
            self.interval_audio(self.correct_answer)
        if self.succeed:
            return False
        if self.time > 6 or self.fail:

            return False
