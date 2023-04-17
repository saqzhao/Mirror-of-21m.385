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
        self.current_level = 0
        self.on_ladder = False
        self.already_resting = False
    
    def walk(self, direction):
        '''
        animates character walking left/right state
        '''
        if self.pos+direction < 0 or self.pos+direction>Window.width:
            # check if at left and right wall, animate "walking but doesn't move"
            pass
        else:
            self.walking = True
            self.remove(self.character)
            real_direction = -1 if direction == Direction.LEFT else 1
            self.pos[0] += real_direction
            self.add(self.character)

    def on_button_down(self, button_value):
        if button_value == 'up':
            self.climb(self.pos)
        elif button_value == 'down':
            self.climb(self.pos)
        elif button_value == 'left':
            self.walk(-1)
        elif button_value == 'right':
            self.walk(1)

    def rest(self, direction):
        '''
        animates character resting state
        '''
        if not self.already_resting:
            # pass
            rest_state = self.rest_left_character if (direction == Direction.LEFT) else self.rest_right_character
            # insert rest state character image here

    def on_button_up(self, button_value):
        if button_value in {'up', 'down', 'left', 'right'}:
            if self.moving_direction in {Direction.UP, Direction.DOWN}:
                if not self.on_ladder: #if at top of ladder, stops climbing, otherwise stops in place on ladder
                    self.moving_direction = Direction.LEFT
                    self.rest(self.moving_direction)
            elif self.moving_direction in {Direction.LEFT, Direction.RIGHT}:
                self.rest(self.moving_direction)
                self.moving = False

    def climb_up(self, pos):
        '''
        animates character climbing up state
        '''
        # Returns True if player is on a ladder spot and can climb up
        if self.background.can_climb(pos) or self.moving:
            self.moving = True
            self.on_ladder = True
            # animate climbing
            if self.character_frame % 2 == 0:
                pass
            else:
                pass
        
            # check if reach top of ladder and if so, don't move
        else:
            self.rest(self.moving_direction)
    
    def climb_down(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        return self.background.can_descend(pos)

    def on_resize(self, win_size):
        pass #TODO

    def on_update(self):
        if self.walking or self.climbing:
            if self.moving_direction == Direction.UP:
                self.climb_up(self.pos)
            elif self.moving_direction == Direction.DOWN:
                self.climb_down(self.pos)
            else:
                self.walk(self.moving_direction)