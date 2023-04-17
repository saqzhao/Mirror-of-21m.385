import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Texture
from kivy.core.window import Window
from kivy.core.image import Image

from Serenade import Direction

class CharacterDisplay(InstructionGroup):
    '''
    Creates player character and controls movement
    '''
    def __init__(self, background) -> None:
        super(CharacterDisplay, self).__init__()
        self.background = background
        self.pos = (0, 0)

        self.character = CEllipse(cpos = self.pos) # temporary 
        # character animation
        self.walk_left_texture = Texture.create(size=(64, 64))
        self.rest_left_character = Image(source='../data/rest_left_character.png', keep_data = True)
        self.rest_right_character = Image(source='../data/rest_right_character.png', anim_delay = 0, keep_data = True)

        self.walk_left_character = Image(source='../data/walk_left_character.gif', anim_delay = 0, keep_data = True)
        self.walk_left_characte.bind(texture=self.update_walk_left_texture)

        self.walk_right_character = Image(source='../data/walk_right_character.gif', anim_delay = 0, keep_data = True)
        self.walk_right_characte.bind(texture=self.update_walk_right_texture)

        self.climb_character = Image(source='../data/climb_character.gif', anim_delay = 0, keep_data = True)
        self.climb_characte.bind(texture=self.update_climb_texture)

        self.cur_character = self.rest_character

        # character movement
        self.character_frame = 0 #0: left, 1:right
        self.moving = False
        self.moving_direction = 0
        self.current_layer = 0
        self.on_ladder = False
        self.already_resting = False
    
    def on_button_down(self, button_value):
        if button_value == 'up':
            self.moving_direction = Direction.UP
            self.climb(self.pos, 1)
        elif button_value == 'down':
            self.moving_direction = Direction.DOWN
            self.climb(self.pos, -1)
        elif button_value in 'left':
            self.moving_direction = Direction.LEFT
            self.walk(self.moving_direction)
        elif button_value == 'right':
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

    def walk(self, direction):
        '''
        animates character walking left/right state
        '''
        if not self.on_ladder:
            if self.pos+direction < 0 or self.pos+direction>Window.width:
                # check if at left and right wall, animate "walking but doesn't move"
                pass
            else:
                self.moving = True
                self.remove(self.character)
                real_direction = -1 if direction == Direction.LEFT else 1
                self.pos[0] += real_direction
                self.add(self.character)

    # animates character climbing up/down state
    def climb(self, pos, direction):
        if self.moving or self.background.can_climb(pos) or self.background.can_descend(pos):
            direction
            self.moving = True
            self.on_ladder = True
            # animate climbing
            self.pos[1] += direction
            ###### ANIMATION HERE
        
            # check if reach end of ladder and if so, stop climbing
            ladder_end = 'T' if direction == 1 else 'B'
            if self.background.distance_to_ladder_end(self.pos[1], ladder_end) < Window.height/30:
                self.on_ladder = False
                self.rest()
        else:
            self.rest(self.moving_direction)

    def on_resize(self, win_size):
        pass #TODO

    # animate character (position and animation) based on current time
    def on_update(self):
        if self.moving:
            if self.moving_direction == Direction.UP:
                self.climb_up(self.pos)
            elif self.moving_direction == Direction.DOWN:
                self.climb_down(self.pos)
            else:
                self.walk(self.moving_direction)