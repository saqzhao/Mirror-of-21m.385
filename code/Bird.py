import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
# from kivy.graphics import Line, CEllipse
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
import random
import math
# from enum import Enum
from Direction import Direction
from Background import BackgroundDisplay

# TODO: Figure out optimal self.pace, etc
class Bird(InstructionGroup):
    def __init__(self, background, pos, call_interval_quiz, character) -> None:
        super(Bird, self).__init__()
        # Storing Variables
        self.character = character
        self.background = background
        self.background.add(self) # Does this work?
        self.call_interval_quiz = call_interval_quiz

        # Position, Location, Movement
        self.x=pos[0]
        self.y=pos[1]
        self.direction = Direction.RIGHT 
        self.pace = Window.width/4/2 # Position per time

        # Things for Interval Quiz 
        self.active = False
        self.range = Window.width/10 # Distance that activates interval quiz
        # self.pace = Window.width/4/5 # Position per time

        # Visual Object
        self.radius = Window.width/50
        self.circle = Ellipse(pos = (self.x, self.y), radius = (self.radius, self.radius))
        self.color = Color(rgb = (.5,.5,.5))
        self.add(self.color)
        self.add(self.circle)

    def player_in_range(self): # Returns TRUE if player and bird are close together
        player_pos = self.character.to_screen_pos()
        is_close = (math.sqrt((self.x-player_pos[0])**2+(self.y-player_pos[1])**2) <= self.range)
        if not is_close:
            return False
        if self.direction == Direction.DOWN: 
            # Player is below and close
            if player_pos[1] < (self.y + self.radius*2):
                return True
        elif self.direction == Direction.RIGHT:
            # Player is to right and close
            if player_pos[0] > self.x and (abs(player_pos[1]-self.y)<self.background.layer_spacing):
                return True
        elif self.direction == Direction.LEFT:
            # Player is to left and close
            if player_pos[0] < self.x and (abs(player_pos[1]-self.y)<self.background.layer_spacing):
                return True
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
        # print(f"moving in {direction} {amount} amount")
        if direction == Direction.RIGHT:
            self.x +=amount
        else:
            self.x -= amount
        self.x = self.x % Window.width

    def update_position(self):
        self.circle.pos= (self.x, self.y)   

    def move_bird(self, move_amt):
        while move_amt > 0: #allows us to, say, go down a tad and then go right on same dt
            # Already going down
            if self.direction == Direction.DOWN: 
                amount = min(self.background.distance_to_ladder_end((self.x, self.y), 'B'), move_amt) # go down until you hit bottom of ladder
                self.move_down(amount)
                move_amt -=amount
                if self.background.distance_to_ladder_end((self.x, self.y), 'B') == 0: # if we've hit bottom of ladder
                    self.direction = random.choice([Direction.RIGHT, Direction.LEFT])
            # Can go down
            elif self.background.can_descend((self.x, self.y)) and (self.direction == Direction.RIGHT or self.direction ==Direction.LEFT):
                if random.random() <.8: # Randomly doesn't  fly down
                    # print("should be going down now")
                    self.direction = Direction.DOWN
                    self.move_down(move_amt)
                    break
                else:
                    # print("not changing to down")
                    self.move_x(move_amt, self.direction)
                    move_amt = 0
            # Go to side
            else:
                self.move_x(move_amt, self.direction)
                move_amt = 0

    def on_update(self, dt):
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
        return True

        
    def on_resize(self, win_size):
        #TODO: This affects bird size, their current position, and rate/multiplier
        pass 

if __name__ == "__main__":
    print("you have entered Bird.py. You are probably running the wrong .py file")
    background = BackgroundDisplay()
    bird = Bird(background)
    print(bird)
