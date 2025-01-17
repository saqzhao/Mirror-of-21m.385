import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CRectangle, KFAnim, AnimGroup

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import random

class QuizButton(Widget):
    def __init__(self, buttonLabel, pos, is_correct, size, callback):
        super(QuizButton, self).__init__()
        self.btn = Button(text = buttonLabel,
                     font_size = "20sp",
                     background_color = (1, 1, 1, 1),
                     color = (1, 1, 1, 1),
                     size = size,
                     size_hint = (0.2, 0.2),
                     pos = pos)
        # background_down and normal must be string address for button (for future style sthing)
        self.is_correct = is_correct
        self.callback = callback
        self.btn.bind(on_press = self.give_result)
        self.add_widget(self.btn)
    

    def give_result(self, _):
        self.background_color = (1, 0, 0, 1) if self.is_correct else (0.5, 0.5, 0.5, 1)
        self.callback(self.is_correct)

    def set_pos(self, pos):
        self.btn.pos=pos

class IntervalQuiz(Widget):
    def __init__(self, mode, options, increment_score, audio_ctrl):
        super(IntervalQuiz, self).__init__()
        self.mode = mode
        self.options = list(options)
        self.timer_color = Color(1, 0, 0)
        self.anim_group = AnimGroup()
        self.canvas.add(self.anim_group)
        self.timer_bar = CRectangle(cpos=(Window.width/2, Window.height/8), csize = (Window.width/3, Window.height/30))
        self.timer_runout = KFAnim((0, Window.width/3, Window.height/30), (6, 0, Window.height/30))
        self.score_func = increment_score
        self.remove_quiz = False
        self.audio_ctrl = audio_ctrl
        self.succeed = False
        self.time = 0
        self.correct_answer = None
        self.interval_being_played = False
        self.already_answered = False

        # quiz buttons
        self.button_size = (Window.width/15, Window.height/20)
        self.button_centerline_margin = Window.width/20
        self.button_distance = self.button_size[0]*1.3
        self.button_locations = [(Window.width/3, Window.width/4), (Window.width/3, Window.width/2), (Window.width*2/3, Window.width/4), (Window.width*2/3, Window.width/2)]

        self.buttons = []
        self.button_labels = []
        self.background_color = Color(1, 1, 1, 0.25)
        self.background = Rectangle(pos=(0, 0), size=(Window.width, Window.height))
        self.quiz_begun = False
        self.time_since_noise_played=0

    def generate_quiz_options(self, num_options):
        options = set()
        self.already_answered = False
        self.canvas.add(self.background_color)
        self.canvas.add(self.background)
        self.canvas.add(self.timer_color)
        self.canvas.add(self.timer_bar)
        if len(self.options) > num_options:
            while (len(options) <= num_options):
                idx_to_add = random.randint(0, len(self.options)-1)
                if idx_to_add not in options:
                    options.add(self.options[idx_to_add])
        else:
            options = self.options
        options = list(options)
        correct_idx = random.randint(0, len(options)-1)

        correct = options[correct_idx]
        return correct, options

    def quiz_result(self, is_correct):
        if not self.already_answered:
            self.already_answered = True
            self.score_func(is_correct, self.correct_answer)
            if is_correct:
                self.audio_ctrl.interval_quiz_success()
                self.remove_quiz = True

    def create_buttons(self, locations, options, correct_answer):
        for loc, opt in zip(locations, options):
            is_correct = False if opt != correct_answer else True
            button = QuizButton(opt, loc, is_correct, self.button_size, self.quiz_result)
            self.buttons.append(button)
            self.add_widget(button)

    def generate_quiz(self):
        self.quiz_begun = True
        if self.mode == 'easy':
            self.correct_answer, all_options = self.generate_quiz_options(4)
            # num_options = len(all_options)
        #     easy_button_locations = [self.button_locations[idx] for idx in range(num_options)]
            self.create_buttons(self.button_locations, all_options, self.correct_answer)
                
        # else:
        #     self.correct_answer = random.choice(self.options)
        #     hard_button_locations = [self.button_locations[idx] for idx in range(len(self.options))]
        #     self.create_buttons(hard_button_locations, self.options, self.correct_answer)

    def on_resize(self, win_size):
        self.background.size = win_size
        if self.quiz_begun:
            width = win_size[0]
            height = win_size[1]

            self.timer_bar.cpos = (width/2, height/8)
            self.timer_bar.csize = (width/3, height/30)
            self.timer_runout = KFAnim((0, width/3, height/30), (6, 0, height/30))

            self.button_size = (width/15, height/20)
            self.button_centerline_margin = width/20
            self.button_distance = self.button_size[0]*1.3
            self.button_locations = [(width/3, width/4), (width/3, width/2), (width*2/3, width/4), (width*2/3, width/2)]
            self.reset_button_locations()


    def reset_button_locations(self):
        print("should be resetting button locations")
        for button, loc, in zip(self.buttons, self.button_locations):
            button.set_pos(loc)


    def on_update(self, dt):
        if self.quiz_begun:
            if not self.interval_being_played:
                self.interval_being_played = True
                self.audio_ctrl.play_interval(self.correct_answer)
            self.time += dt
            self.timer_bar.csize = self.timer_runout.eval(self.time)
            if self.remove_quiz:
                self.audio_ctrl.stop()
                self.remove_quiz = False
                return
            if self.time > 6:
                self.audio_ctrl.stop()
                if not self.already_answered:
                    self.score_func(False, self.correct_answer)
                return False
            return True
        else:
            pass
