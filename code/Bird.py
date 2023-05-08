import sys, os
sys.path.insert(0, os.path.abspath('..'))

# from kivy.graphics import Line, CEllipse
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
import random
import math
# from enum import Enum
from Direction import Direction
from Background import BackgroundDisplay
from kivy.uix.image import Image
from kivy.uix.widget import Widget


# TODO: Figure out optimal self.pace, etc
class Bird(Widget):
    def __init__(self, background, pos, call_interval_quiz, character) -> None:
        super(Bird, self).__init__()
        self.character = character
        self.background = background
        self.call_interval_quiz = call_interval_quiz

        # Position, Location, Movement
        self.x=pos[0]
        self.y=pos[1]
        self.direction = Direction.RIGHT 
        self.next_direction = Direction.RIGHT
        self.pace = Window.width/4/2 # Position per time

        self.freeze = False

        # Visual Object
        self.bird_left = '../data/bird_left.gif'
        self.bird_right = '../data/bird_right.gif'
        self.bird = Image(source = self.bird_right, anim_delay=0, keep_data = True)
        self.add_widget(self.bird)
        self.background.add_widget(self) # Does this work?

        # Interval Quiz 
        self.active = False

        self.times_around_this_level =0

        self.old_window_width = Window.width
        self.old_window_height = Window.height

        self.range = 50

        print(f"bird info: size is {self.size}")

    def toggle(self):
        if not self.freeze:
            self.freeze = True
        else:
            self.freeze = False

    def player_in_range(self): # Returns TRUE if player and bird are close together
        player_pos = self.character.to_screen_pos()
        # if self.collide_widget(self.character):
        #     print("COLLISION")
        #     print(self.x, self.y, player_pos)
        #     return True
        # if self.collide_point(player_pos[0], player_pos[1]):
        #     print("collide point")
        # print(self.center_x, self.x, self.x+self.size[0])
        center_x = self.x+self.size[0]/2 # accounts for size of 
        is_close = (math.sqrt((center_x-player_pos[0])**2+(self.y-player_pos[1])**2) <= self.range)
        # if self.collide_widget(self.character) and is_close:
        #     print("correct!")
        if is_close:
            return True
        # if not is_close:
        #     return False
        # if self.direction == Direction.DOWN: 
        #     # Player is below and close
        #     if player_pos[1] < (self.y + self.radius*2):
        #         return True
        # elif self.direction == Direction.RIGHT:
        #     # Player is to right and close
        #     return True
        #     if player_pos[0] > self.x and (abs(player_pos[1]-self.y)<self.background.layer_spacing):
        #         return True
        # elif self.direction == Direction.LEFT:
        #     # Player is to left and close
        #     return True
        #     if player_pos[0] < self.x and (abs(player_pos[1]-self.y)<self.background.layer_spacing):
        #         return True
        return False

    def hit_bird(self):
        self.active = True
        self.call_interval_quiz()

    def send_pos(self):
        return (self.x, self.y)
    
    def move_down(self, amount):
        self.y-= amount
        pass

    def move_x(self, amount: float|int, direction: Direction):
        if direction == Direction.RIGHT:
            self.x +=amount
        else:
            self.x -= amount
        x = self.x % Window.width

        # counting how many times a bird goes in circles so that it only cycles twice
        if self.x!=x:
            self.times_around_this_level +=1
        self.x=x

    def update_position(self):
        self.bird.pos[0] = self.x 
        self.bird.pos[1] = self.y

    def move_bird(self, move_amt):
        if not self.freeze:
            while move_amt > 0: #allows us to, say, go down a tad and then go right on same dt
                # Already going down
                if self.direction == Direction.DOWN: 
                    amount = min(self.background.distance_to_ladder_end((self.x, self.y), 'B'), move_amt) # go down until you hit bottom of ladder
                    self.move_down(amount)
                    move_amt -=amount
                    if self.background.distance_to_ladder_end((self.x, self.y), 'B') == 0: # if we've hit bottom of ladder
                        self.direction = self.next_direction
                # Can go down
                elif self.background.can_descend((self.center_x, self.y)) and (self.direction == Direction.RIGHT or self.direction ==Direction.LEFT):
                    if random.random() <.8: # Randomly doesn't  fly down
                        self.direction = Direction.DOWN
                        self.times_around_this_level = 0
                        self.next_direction = random.choice([Direction.RIGHT, Direction.LEFT])
                        self.bird.source = self.bird_right if self.next_direction == Direction.RIGHT else self.bird_left
                        self.move_down(move_amt)
                        break
                    else:
                        self.move_x(move_amt, self.direction)
                        move_amt = 0
                # Go to side
                else:
                    self.move_x(move_amt, self.direction)
                    move_amt = 0

    def on_update(self, dt):
        if not self.freeze:
            move_amt = self.pace*dt

            if not self.active: 
                x=self.player_in_range()
                if x:
                    self.hit_bird()
                    return
            if self.active:
                return False
            self.move_bird(move_amt) 
            self.update_position()
            if self.times_around_this_level >=2:
                return False
        return True


    def on_resize(self, win_size):
        #TODO: This affects bird size, their current position, and rate/multiplier
        self.x *= win_size[0]/self.old_window_width
        self.y *= win_size[1]/self.old_window_height
        self.old_window_width, self.old_window_height = win_size
        self.update_position()

if __name__ == "__main__":
    background = BackgroundDisplay()
    character = "hds"
    def quiz(): #what is this doing?
        return "hi"
    bird = Bird(quiz, (400,400),background, character)
