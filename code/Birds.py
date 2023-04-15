import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line, CEllipse
from kivy.core.window import Window
import random
from enum import Enum


class Birds(InstructionGroup):
    def __init__(self, IntervalQuiz, Background) -> None:
        super(Birds, self).__init__()
        self.x=0
        self.y=0
        self.direction = Direction.RIGHT # True for Right, False for Left
        self.active = False
        self.range = 50 # Distance in pixels that activates interval quiz
        self.background = Background

    def player_in_range(self, pos): # May/May not use
        player_height =10
        if abs(self.y-pos[1])<player_height and abs(self.x -pos[0])<self.range:
            print("Player and barrel are close")
            # IntervalQuiz.start()

    def send_pos(self):
        return (self.x, self.y)

    def on_update(self, time):
        if self.background.above_ladder():
            go_down = True if random.random()<0.7 else False # Some logic for whether or not the birds/barrel falls
            # go_down = True if there's another barrel in the same lane
        

    def on_resize(self, win_size):
        pass #TODO
