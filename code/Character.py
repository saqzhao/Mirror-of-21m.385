import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle
from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image

from Direction import Direction

directions = {member for member in Direction}

class Character(Widget):
    '''
    Creates player character and controls movement
    '''
    def __init__(self, background) -> None:
        super(Character, self).__init__()
        self.background = background
        self.pos = (0, 0)
        self.tim = Image(source='../data/tim.png', pos = (Window.width / 12, Window.height - 1.1*Window.height / 8))
        self.add_widget(self.tim)
        
        # character animation
        self.rest_left_character = '../data/rest_left.png'
        self.rest_right_character = '../data/rest_right.png'
        self.walk_left_character = '../data/walk_left.gif'
        self.walk_right_character = '../data/walk_right.gif'
        self.climb_character = '../data/climb.gif'
        self.character = Image(source=self.rest_right_character, anim_delay=0, keep_data = True, pos = (Window.width / 10, Window.height / 10))
        
        # character movement
        self.moving = False
        self.moving_direction = 0
        self.on_ladder = False
        self.frozen = False
        self.margin_side = Window.width / 10
        
        self.add_widget(self.character)
    
    
    def on_button_down(self, button_value):
        if self.frozen:
            print('hi')
            pass
        if button_value in {Direction.UP, Direction.DOWN}:
            self.moving_direction = button_value
            self.climb(self.moving_direction)
        elif button_value in {Direction.LEFT, Direction.RIGHT}:
            self.moving_direction = button_value
            self.walk(self.moving_direction)

    def on_button_up(self, button_value):
        if button_value in directions:
            self.moving = False
            if self.moving_direction in {Direction.UP, Direction.DOWN}:
                if not self.on_ladder: #if at top of ladder, stops climbing, otherwise stops in place on ladder
                    self.moving_direction = Direction.LEFT
                    self.rest(self.moving_direction)
            else:
                self.rest(self.moving_direction)

    def reset(self):
        self.character = Image(source=self.rest_right_character, anim_delay=0, keep_data = True, pos = (Window.height / 10, Window.width / 10))
        self.frozen = False
        self.moving = False
        self.on_ladder = False
        self.moving_direction = 0

    def freeze(self):
        print('character freeze')
        self.frozen = True

    def unfreeze(self):
        print('character unfreeze')
        self.frozen = False

    def rest(self, direction = Direction.LEFT):
        '''
        animates character resting state
        '''
        self.moving = False
        self.character.source = self.rest_left_character if (direction == Direction.LEFT) else self.rest_right_character

    def walk(self, moving_direction):
        '''
        animates character walking left/right state
        '''
        if self.frozen:
            return
        if not self.on_ladder:
            direction = 1
            if moving_direction == Direction.LEFT:
                direction = -1
                self.character.source = self.walk_left_character
            else:
                self.character.source = self.walk_right_character

            if self.character.pos[0]+direction < self.margin_side or self.character.pos[1]+direction>Window.width-self.margin_side:
                # check if at left and right wall, animate "walking but doesn't move"
                pass
            else:
                self.moving = True
                self.character.pos[0] += direction

    def to_screen_pos(self):
        x = self.character.pos[0]+Window.width/20
        y = self.character.pos[1]
        return (x, y)

    # animates character climbing up/down state
    def climb(self, moving_direction):
        if self.frozen:
            return
        screen_pos = self.to_screen_pos()
        direction = 1 if moving_direction == Direction.UP else -1
        if (self.background.can_climb(screen_pos) and direction ==1) or (self.background.can_descend(screen_pos) and direction ==-1):
            self.character.source = self.climb_character
            # direction
            self.moving = True
            self.on_ladder = True
            # move character
            ladder_end = 'T' if direction == 1 else 'B'

            # problem was when you get to the top of the ladder you go up an extra step
            fraction = self.background.distance_to_ladder_end(screen_pos, ladder_end)
        
            # Because whole numbers don't always happen
            if fraction <= 1 and fraction >0: 
                self.character.pos[1] += fraction * direction
            else:
                 self.character.pos[1] += direction

            # check if reach end of ladder and if so, stop climbing
            new_screen_pos = self.to_screen_pos()
            if self.background.distance_to_ladder_end(new_screen_pos, ladder_end) == 0:
                self.on_ladder = False
                self.rest()

        elif self.background.can_climb(screen_pos) or self.background.can_descend(screen_pos):
            self.on_ladder = False
            self.rest()
        else:
            self.rest(self.moving_direction)

    def on_resize(self, win_size):
        pass #TODO

    # animate character (position and animation) based on current time
    def on_update(self):
        if self.moving:
            if self.moving_direction in {Direction.UP, Direction.DOWN}:
                self.climb(self.moving_direction)
            else:
                self.walk(self.moving_direction)
        x, y = self.to_screen_pos()
        return (y >= 600 and x <= 120)
        