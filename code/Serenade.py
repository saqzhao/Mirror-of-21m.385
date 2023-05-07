import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import lookup
from imslib.screen import Screen
from kivy.clock import Clock as kivyClock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget

from Background import BackgroundDisplay
from Bird import Bird
from CollectedInstrument import CollectedInstrumentDisplay
from Direction import Direction
from Character import Character
from IntervalQuiz import IntervalQuiz
from AudioController import AudioController
from FinalScreenAudioController import FinalScreenAudioController
from QuizDisplay import QuizDisplay
from PauseButton import PauseButton
from Help import HelpButton

import random

# Scaling Constants we will be working with
ladder_w = 0.1
ramp_h = 0.75*ladder_w
player_h = 4*ramp_h
directions = {member.value for member in Direction}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(always_update=True, **kwargs)
        self.canvas.clear()
        self.started = True
        self.audio_ctrl = AudioController()
        self.final_song_audio_ctrl = FinalScreenAudioController()
        self.background = BackgroundDisplay()
        self.character = Character(self.background)
        self.quiz_display = QuizDisplay()
        self.ended = False
        print('start game')

        self.default_intervals = {'2M', '3M', '4', '5'}
        self.intervals = set()

        intervals = self.default_intervals if (len(self.intervals) == 0) else self.intervals
        self.player = Player(self.audio_ctrl, self.final_song_audio_ctrl, self.background, self.character, self.quiz_display, intervals, self)
        self.add_widget(self.player)

    def toggle(self):
        self.player.toggle()

    def select_intervals(self, interval, add = True):
        if not add:
            self.intervals.remove(interval)
            print("intervals are now ", self.intervals)
            return
        self.intervals.add(interval)
        print("intervals are now ", self.intervals)

    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'enter':
            self.switch_to('end') # delete once done testing

        # play / pause toggle
        if keycode[1] == 'p':
            self.toggle()

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
        # resize_topleft_label(self.info)
        self.background.on_resize(win_size)
        self.character.on_resize(win_size)
        #TODO : anything else that needs resizing ?

    def on_update(self):
        if self.started and not self.ended:
            self.audio_ctrl.on_update()
            switch_to_end_screen, game_over = self.player.on_update()
            if not self.ended and switch_to_end_screen:
                self.switch_to('end')
                self.ended = True
            if not self.ended and game_over:
                self.switch_to('game_over')
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
        self.started = True
        self.audio_ctrl = AudioController()
        self.final_song_audio_ctrl = FinalScreenAudioController()
        self.background = BackgroundDisplay()
        self.character = Character(self.background)
        self.quiz_display = QuizDisplay()
        intervals = self.default_intervals if (len(self.intervals) == 0) else self.intervals
        self.player = Player(self.audio_ctrl, self.final_song_audio_ctrl, self.background, self.character, self.quiz_display, intervals, self)
        self.add_widget(self.player)
        self.ended = False
        print('start game')


class Player(Widget):
    '''
    Handles game logic
    Controls the GameDisplay and AudioCtrl based on what happens
    '''

    def __init__(self, audio_ctrl, final_song_audio_ctrl, background, character, quiz_display, intervals, screen):
        super(Player, self).__init__()
        # self.clock = kivyClock()
        # self.clock = serenClock
        self.screen = screen
        self.background = background
        self.quiz_display = quiz_display
        self.audio_ctrl = audio_ctrl
        self.final_song_audio_ctrl = final_song_audio_ctrl
        self.character = character
        self.add_widget(self.background)
        self.add_widget(self.quiz_display)
        self.add_widget(self.character)

        self.pause_button = PauseButton(self.toggle, self.screen)
        self.add_widget(self.pause_button)
        self.help_button = HelpButton(self.screen, self.toggle)
        self.add_widget(self.help_button)

        self.score = 0
        self.mode = 'easy'        
        self.time=0
        self.num_collected_so_far = 0
        self.instruments = ["violin", "guitar", "piano"]
        self.x_centers_to_avoid = []
        self.lives = 3
        self.background.add_lives(3)    
        self.game_over = False

        self.freeze = False
        self.pause_time = 0

        # Birds
        self.birds_spawned = 0
        self.birds = []

        # Collectables
        self.collectables = self.make_collectables(3)

        # Interval 
        self.options = intervals 
        # self.quiz_active = False
        self.quiz = None

    def make_collectables(self, num_collectables):
        collect = set()
        for collectable_name_idx in range(num_collectables):
            layer = random.randint(0, 6)
            this_collectable = CollectedInstrumentDisplay(self.background, self.character, self.instruments[collectable_name_idx], layer, self.on_instrument_collected, self.x_centers_to_avoid)
            self.x_centers_to_avoid.append(this_collectable.get_x_pos())
            collect.add(this_collectable)
        return collect

    def toggle(self):
        print('entering player toggle')
        if not self.freeze:
            print('pausing in player')
            self.freeze = True
            # self.pause_time = self.clock.time()
            self.character.freeze()
            for bird in self.birds:
                bird.toggle()
            print('done running freeze')
        else:
            print('unpausing in player')
            self.freeze = False
            self.character.unfreeze()
            for bird in self.birds:
                bird.toggle()
            print('done running unpause')

    # called by IntervalQuiz
    def adjust_lives(self, succeed, interval):
        self.character.unfreeze()
        if not succeed:
            if self.lives > 1:
                self.lives -= 1
                self.background.lose_life()
            else:
                self.game_over = True
                print('Sorry, you have crashed into too many birds, try again?')

        else:
            self.background.add_one_to_count() # increments count of correct intervals guessed
        if interval is not None:
            self.final_song_audio_ctrl.add_interval(interval)

    def reset(self):
        self.background.reset()
        self.character.reset()
        self.collectables = self.make_collectables(3)
        self.lives = 3
        self.game_over = False
        self.freeze = False
        self.quiz = None

    # called by Bird
    def call_interval_quiz(self):
        self.character.freeze()
        self.quiz = IntervalQuiz(self.mode, self.options, self.adjust_lives, self.audio_ctrl)
        self.quiz_display.add_quiz(self.quiz)
        self.audio_ctrl.hit_bird()
        self.quiz.generate_quiz()
        # self.quiz_active = True
    
    # called by MainWidget
    def on_button_down(self, button_value):
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_down(direction)

    # called by MainWidget
    def on_button_up(self, button_value):
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_up(direction)

    def spawn_bird(self):
        if not self.freeze:
            new_bird = Bird(self.background, (Window.width *0.8, self.background.get_start_position_height()), self.call_interval_quiz, self.character)
            self.birds.append(new_bird)
            self.birds_spawned+=1

    def on_update(self):
        # if self.game_over:
        #     self.reset()
        #     return False
        switch_to_end_screen = False
        if not self.freeze:
            dt =  kivyClock.frametime
            # dt = self.clock.get_time()
            if self.quiz != None:
                x=self.quiz.on_update(dt)
                if not x:
                    self.quiz_display.remove_quiz()
                    self.quiz = None
                return (False, False)
            
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
                    self.background.remove_widget(bird)
                    self.birds.remove(bird)
            
            self.final_song_audio_ctrl.on_update()

        return (switch_to_end_screen, self.game_over)

    def on_instrument_collected(self, collectable):
        inst_name = collectable.get_instrument()
        self.final_song_audio_ctrl.on_instrument_collected(inst_name)
        self.background.add_collected(collectable.get_inst_source(), self.num_collected_so_far)
        self.num_collected_so_far += 1
        self.audio_ctrl.collect_instrument(inst_name)