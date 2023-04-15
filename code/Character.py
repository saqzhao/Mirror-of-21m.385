import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image

from Serenade import DIRECTIONS

class CharacterDisplay(InstructionGroup):
    '''
    Creates player character and controls movement
    '''
    def __init__(self, background) -> None:
        super(CharacterDisplay, self).__init__()
        self.background = background
        self.pos = (0, 0)
        self.character = CEllipse(cpos = self.pos) # temporary
        self.moving = False
        self.moving_direction = 0
    
    def walk(self, direction):
        self.pos[0] += 2*direction

    def on_button_down(self, button_value):
        pass #TODO

    def on_button_up(self, button_value):
        pass #TODO

    def climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        return self.background.can_climb(pos)
    
    def descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        return self.background.can_descend(pos)

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self):
        if self.moving:
            if self.moving_direction == DIRECTIONS.right:
                self.walk(-1)
            elif self.moving_direction == DIRECTIONS.right:
                self.walk(1)
            elif self.moving_direction == DIRECTIONS.right:
                self.climb(self.pos)
            elif self.moving_direction == DIRECTIONS.right:
                self.climb(self.pos)
