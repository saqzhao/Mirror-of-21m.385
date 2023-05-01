import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import lookup
from imslib.screen import Screen
from kivy.clock import Clock as kivyClock
from kivy.core.window import Window

from Background import BackgroundDisplay
from Bird import Bird
from CollectedInstrument import CollectedInstrumentDisplay
from Direction import Direction
from Character import Character
from IntervalQuiz import IntervalQuiz
from AudioController import AudioController
from FinalScreenAudioController import FinalScreenAudioController
from QuizDisplay import QuizDisplay

import random

# Scaling Constants we will be working with
ladder_w = 0.1
ramp_h = 0.75*ladder_w
player_h = 4*ramp_h
directions = {member.value for member in Direction}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(always_update=True, **kwargs)
        self.started = False
        self.audio_ctrl = AudioController()
        self.final_song_audio_ctrl = FinalScreenAudioController()
        self.background = BackgroundDisplay()
        self.character = Character(self.background)
        self.quiz_display = QuizDisplay()
        self.add_widget(self.background)
        self.add_widget(self.quiz_display)
        self.default_intervals = {'2M', '3M', '4', '5'}
        self.intervals = set()
        self.player = None
    
    def start(self):
        self.started = True
        if len(self.intervals) == 0:
            self.intervals = self.default_intervals
        self.player = Player(self.audio_ctrl, self.final_song_audio_ctrl, self.background, self.character, self.quiz_display, self.intervals)
        self.add_widget(self.player.character, index=1)
        self.ended = False

    def select_intervals(self, interval):
        self.intervals.add(interval)

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'enter':
            self.switch_to('end') # delete once done testing

        # play / pause toggle
        if keycode[1] == 'p':
            self.player.toggle()
        #     self.audio_ctrl.toggle()

        button_idx = lookup(keycode[1], ['up', 'down', 'left', 'right', 'w', 'a', 's', 'd', 'x'], (0,1,2,3,0, 2,1,3,4))
        if button_idx != None:
            self.player.on_button_down(button_idx)

        if keycode[1] == 'l':
            # Dummy button, will play automatically upon reaching the top
            self.final_song_audio_ctrl.play_serenade()

    def on_key_up(self, keycode):
        button_idx = lookup(keycode[1], ['up', 'down', 'left', 'right', 'w', 'a', 's', 'd', 'x'], (0,1,2,3, 0, 2,1,3,4))
        if button_idx != None:
            self.player.on_button_up(button_idx)


    # handle changing displayed elements when window size changes
    # This function should call GameDisplay.on_resize
    def on_resize(self, win_size):
        pass
        # resize_topleft_label(self.info)
        # self.display.on_resize(win_size)
        #TODO : anything else that needs resizing ?

    def on_update(self):
        if self.started and not self.ended:
            self.audio_ctrl.on_update()
            switch_to_end_screen = self.player.on_update()
            if not self.ended and switch_to_end_screen:
                self.switch_to('end')
                self.ended = True
        elif self.started:
            self.final_song_audio_ctrl.on_update()
        # now = self.audio_ctrl.get_time()  # time of song in seconds.
        # self.player.on_update(now)

        # self.info.text = 'p: pause/unpause song\n'
        # self.info.text += f'song time: {now:.2f}\n'
        # self.info.text += f'num objects: {self.display.get_num_object()}'

    def on_enter(self):
        self.canvas.clear()
        self.audio_ctrl = AudioController()
        self.final_song_audio_ctrl = FinalScreenAudioController()
        self.background = BackgroundDisplay()
        self.character = Character(self.background)
        self.quiz_display = QuizDisplay()
        if len(self.intervals) == 0:
            self.intervals = self.default_intervals
        self.player = Player(self.audio_ctrl, self.final_song_audio_ctrl, self.background, self.character, self.quiz_display, self.intervals)
        self.add_widget(self.background)
        self.add_widget(self.player.character)
        self.add_widget(self.quiz_display)
        self.ended = False


class Player(object):
    '''
    Handles game logic
    Controls the GameDisplay and AudioCtrl based on what happens
    '''

    def __init__(self, audio_ctrl, final_song_audio_ctrl, background, character, quiz_display, intervals):
        super(Player, self).__init__()
        self.background = background
        self.quiz_display = quiz_display
        self.audio_ctrl = audio_ctrl
        self.final_song_audio_ctrl = final_song_audio_ctrl
        self.score = 0
        self.character = character
        self.mode = 'easy'        
        self.time=0
        self.collected_instruments = set()
        self.instruments = ["violin", "guitar", "piano"] # TODO(ashleymg): choose randomly from a selection
        self.x_centers_to_avoid = []
        self.lives = 3
        self.freeze = False

        # Birds
        self.birds_spawned = 0
        self.birds = []

        # Collectables
        self.collectables = set()
        for j in range(3):
            i = random.randint(0, 7)
            this_collectable = CollectedInstrumentDisplay(self.background, self.character, self.instruments[j], i, self.on_instrument_collected, self.x_centers_to_avoid)
            self.x_centers_to_avoid.append(this_collectable.get_x_pos())
            self.collectables.add(this_collectable)

        # Interval 
        self.options = intervals 
        # self.quiz_active = False
        self.quiz = None

    def toggle(self):
        if not self.freeze:
            self.freeze = True
            self.character.freeze()
            for bird in self.birds:
                bird.toggle()
        else:
            self.freeze = False
            self.character.unfreeze()
            for bird in self.birds:
                bird.toggle()

    # called by IntervalQuiz
    def adjust_lives(self, succeed, interval):
        print("called score func with succeed", succeed, "and interval", interval)
        self.character.unfreeze()
        if not succeed:
            self.lives -= 1
        if interval is not None:
            print("now adding interval to final song audio ctrl")
            self.final_song_audio_ctrl.add_interval(interval)

    # called by Bird
    def call_interval_quiz(self):
        self.character.freeze()
        print("calling interval quiz serenade.py")
        self.quiz = IntervalQuiz(self.mode, self.options, self.adjust_lives, self.audio_ctrl.play_interval)
        self.quiz_display.add_quiz(self.quiz)
        self.quiz.generate_quiz()
        # self.quiz_active = True
    
    # called by MainWidget
    def on_button_down(self, button_value):
        if button_value ==5:
            self.testing_something()
            return
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_down(direction)

    # called by MainWidget
    def on_button_up(self, button_value):
        if button_value ==5:
            self.testing_something()
            return
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_up(direction)

    def testing_something(self):
        print("sure something happens here (testing_something serenade.py)")

    def spawn_bird(self):
        if not self.freeze:
            new_bird = Bird(self.background, (Window.width *0.8, self.background.get_start_position_height()), self.call_interval_quiz, self.character)
            self.birds.append(new_bird)
            self.birds_spawned+=1

    def on_update(self):
        dt = kivyClock.frametime
        if self.quiz != None:
            x=self.quiz.on_update(dt)
            if not x:
                self.quiz_display.remove_quiz()
                self.quiz = None
            return

        self.time += dt
        bird_num = int(self.time)/5
        if bird_num > self.birds_spawned:
            self.spawn_bird()

        switch_to_end_screen = self.character.on_update()
        
        for collectable in self.collectables:
            collectable.on_update(dt)

        for bird in self.birds:
            a=bird.on_update(dt)
            if not a:
                print("removing this bird")
                self.background.remove_widget(bird)
                self.birds.remove(bird)
        
        self.final_song_audio_ctrl.on_update()

        return switch_to_end_screen

    def on_instrument_collected(self, collectable):
        self.final_song_audio_ctrl.on_instrument_collected(collectable.get_instrument())