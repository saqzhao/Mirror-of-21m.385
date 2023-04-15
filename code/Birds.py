import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Line, CEllipse
from kivy.core.window import Window

class Birds(InstructionGroup):
    def __init__(self, IntervalQuiz) -> None:
        super(Birds, self).__init__()
        self.x=0
        self.y=0
        self.active = False

    def player_in_range(self, pos):
        pass 

    def send_pos(self):
        pass

    def on_update(self, time):
        pass

    def on_resize(self, win_size):
        pass #TODO
