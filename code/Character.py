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

class Character(Widget):
    '''
    Creates player character and controls movement
    '''
    def __init__(self, background) -> None:
        super(Character, self).__init__()
        self.background = background
        self.pos = (0, 0)

        # self.character = CEllipse(cpos = self.pos) # temporary 
        # character animation
        self.rest_left_character = '../data/rest_left.png'
        self.rest_right_character = '../data/rest_right.png'
        self.walk_left_character = '../data/walk_left.gif'
        self.walk_right_character = '../data/walk_right.gif'
        self.climb_character = '../data/climb.gif'
        self.character = Image(source=self.rest_left_character, anim_delay=0, keep_data = True)

        # self.walk_left_texture = Texture.create(size=(64, 64))
        # self.walk_left.bind(texture=self.update_walk_left_texture)
        # self.walk_right.bind(texture=self.update_walk_right_texture)
        # self.climb.bind(texture=self.update_climb_texture)

        Clock.schedule_interval(self.on_update, 1.0/30.0)

        # character movement
        self.character_frame = 0 #0: left, 1:right
        self.moving = False
        self.moving_direction = 0
        self.current_layer = 0
        self.on_ladder = False
        self.already_resting = False
    
    def __remove_character(self):
        Clock.unschedule(self.update);

    def on_button_down(self, button_value):
        if button_value == Direction.UP:
            self.moving_direction = Direction.UP
            self.climb(self.character.pos, 1)
        elif button_value == Direction.DOWN:
            self.moving_direction = Direction.DOWN
            self.climb(self.character.pos, -1)
        elif button_value == Direction.LEFT:
            self.moving_direction = Direction.LEFT
            self.walk(self.moving_direction)
        elif button_value == Direction.RIGHT:
            self.moving_direction = Direction.RIGHT
            self.walk(self.moving_direction)

    def on_button_up(self, button_value):
        if button_value in {'up', 'down', 'left', 'right'}:
            self.moving = False
            if self.moving_direction in {Direction.UP, Direction.DOWN}:
                if not self.on_ladder: #if at top of ladder, stops climbing, otherwise stops in place on ladder
                    self.moving_direction = Direction.LEFT
                    self.rest(self.moving_direction)
            else:
                self.rest(self.moving_direction)

    def rest(self, direction = Direction.LEFT):
        '''
        animates character resting state
        '''
        self.moving = False
        if not self.already_resting:
            # pass
            rest_state = self.rest_left_character if (direction == Direction.LEFT) else self.rest_right_character
            # insert rest state character image here

    def walk(self, moving_direction):
        '''
        animates character walking left/right state
        '''
        if not self.on_ladder:
            direction = -1
            if moving_direction == Direction.LEFT:
                direction = 1
                self.character.source = self.walk_left_character
            else:
                self.character.source = self.walk_right_character

            if self.characterpos[0]+direction < 0 or self.character.pos[1]+direction>Window.width:
                # check if at left and right wall, animate "walking but doesn't move"
                pass
            else:
                self.moving = True
                self.remove(self.character)
                self.character.pos[0] += direction
                self.add(self.character)


    # animates character climbing up/down state
    def climb(self, moving_direction):
        if self.moving or self.background.can_climb(self.character.pos) or self.background.can_descend(self.character.pos):
            direction = -1
            if moving_direction == Direction.UP:
                direction = 1
                self.character.source = self.climb_character
            else:
                self.character.source = self.climb_character


            direction
            self.moving = True
            self.on_ladder = True
            # animate climbing
            self.character.pos[1] += direction
            ###### ANIMATION HERE
        
            # check if reach end of ladder and if so, stop climbing
            ladder_end = 'T' if direction == 1 else 'B'
            if self.background.distance_to_ladder_end(self.character.pos[1], ladder_end) < Window.height/30:
                self.on_ladder = False
                self.rest()
        else:
            self.rest(self.moving_direction)

    def on_resize(self, win_size):
        pass #TODO

    # animate character (position and animation) based on current time
    def on_update(self):
        if self.moving:
            if self.moving_direction < 2:
                self.climb(self.moving_direction)
            else:
                self.walk(self.moving_direction)