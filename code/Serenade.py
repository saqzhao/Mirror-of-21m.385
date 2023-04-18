import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.audio import Audio
from imslib.synth import Synth
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle
from kivy.clock import Clock as kivyClock
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image

from enum import Enum

from Background import BackgroundDisplay
from Bird import Bird
from Direction import Direction
from Character import Character
from IntervalQuiz import IntervalQuiz


# Scaling Constants we will be working with
ladder_w = 0.1
ramp_h = 0.75*ladder_w
player_h = 4*ramp_h
directions = {member.value for member in Direction}


class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.audio_ctrl = Audio(2) # TODO - rename to self.audio if we don't use the controller
        self.background = BackgroundDisplay()
        self.character = Character(self.background)
        # self.player = Player(self.audio_ctrl, self.background)
        self.player = Player(self.audio_ctrl, self.background)
        self.canvas.add(self.background)
        self.add_widget(self.player.character)

    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.audio_ctrl.toggle()

        # button down TODO: Change to arrow keys or controller controls
        # button_idx = lookup(keycode[1], 'wasd', (0,1,2,3))
        button_idx = lookup(keycode[1], ['up', 'down', 'left', 'right'], (0,1,2,3))
        if button_idx != None:
            self.player.on_button_down(button_idx)

    def on_key_up(self, keycode):
        # button up
        # button_idx = lookup(keycode[1], 'wasd', (0,1,2,3))
        button_idx = lookup(keycode[1], ['up', 'down', 'left', 'right'], (0,1,2,3))
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
        self.audio_ctrl.on_update()
        self.player.on_update()
        # now = self.audio_ctrl.get_time()  # time of song in seconds.
        # self.player.on_update(now)

        # self.info.text = 'p: pause/unpause song\n'
        # self.info.text += f'song time: {now:.2f}\n'
        # self.info.text += f'num objects: {self.display.get_num_object()}'

class Player(object):
    '''
    Handles game logic
    Controls the GameDisplay and AudioCtrl based on what happens
    '''

    def __init__(self, audio_ctrl, background):
        super(Player, self).__init__()
        self.background = background
        self.audio_ctrl = audio_ctrl
        self.score = 0
        self.character = None
        self.mode = 'easy'
        self.birds = []
        self.time=0
        self.options = ['2M', '3M', '4', '5'] ### need to have a way for player to choose what
                                                ## intervals they want to be quizzed on
        self.birds_spawned =0

    def increment_score(self, succeed):
        magnifier = 1 if succeed else 0
        self.score += 10*magnifier
        self.total += 10

    def start_game(self):
        self.character = Character(self.background)

    # called by MainWidget
    def on_button_down(self, button_value):
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_down(direction)
    
    def call_interval_quiz(self):
        interval_quiz = IntervalQuiz(self.mode, self.options, self.increment_score, self.audio_ctrl.play_interval)


    # called by MainWidget
    def on_button_up(self, button_value):
        for direction in Direction:
            if button_value == direction.value:
                self.character.on_button_up(direction)

    def spawn_bird(self):
        # print("Spawning a new bird")
        new_bird = Bird(self.background, (Window.width *0.8, self.background.get_start_position_height()), self.call_interval_quiz)
        self.birds.append(new_bird)
        self.birds_spawned+=1

    def on_update(self):
        # self.background.on_update(self.time)
        dt = kivyClock.frametime
        self.time += dt
        bird_num = int(self.time)/5
        if bird_num > self.birds_spawned:
            self.spawn_bird()

        for bird in self.birds:
            bird.on_update(dt)
        self.character.on_update()


if __name__ == "__main__":
    run(MainWidget())
