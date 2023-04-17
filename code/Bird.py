import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.graphics.instructions import InstructionGroup
# from kivy.graphics import Line, CEllipse
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
import random
import math
# from enum import Enum
from Serenade import Direction
from Background import BackgroundDisplay

print("you have entered Bird.py. You are probably running the wrong .py file")

# TODO: Figure out optimal self.pace, etc
class Bird(InstructionGroup):
    def __init__(self, background, pos = (0,0)) -> None:
        super(Bird, self).__init__()
        self.background = background
        self.x=pos[0]
        self.y=pos[1]
        self.direction = Direction.RIGHT 
        self.active = False
        self.range = 50 # Distance in pixels that activates interval quiz
        self.pace = 1 # Position per time
        self.radius = 10
        self.circle = Ellipse(pos = (self.x, self.y), radius = (self.radius, self.radius))
        self.add(self.circle)

    def player_in_range(self, pos): # May/May not use
        # If euclidean distance close
        # OR If barrel moving Towards player on flat or going down and close to player
        is_close = (math.sqrt((self.x-pos[0])**2+(self.y-pos[1])**2) <= self.range)
        if not is_close:
            return False

        if self.direction == Direction.DOWN:
            # Player is beneath and also close
            if pos[1] < (self.y +self.height*2):
                # If interval quiz is passed into bird, call it here
                return True
        elif self.direction == Direction.RIGHT:
            # Player is to right and close
            if pos[0] > self.x and (abs(pos[1]-self.y)<self.background.layer_spacing):
                return True
        elif self.direction == Direction.LEFT:
            # Player is to left and close
            if pos[0] < self.x and (abs(pos[1]-self.y)<self.background.layer_spacing):
                return True

        return False

    def send_pos(self):
        return (self.x, self.y)
    
    def move_down(self, amount):
        print(f"moving down {amount}")
        self.y-= amount
        pass

    def move_x(self, amount, direction):
        print(f"moving in {direction} {amount} amount")
        if direction == Direction.RIGHT:
            self.x +=amount
        else:
            self.x -= amount
        self.x = self.x % Window.width

    def update_position(self):
        print(f"updating position to x: {self.x}, y: {self.y}")
        self.circle.pos= (self.x, self.y)        

    def on_update(self, dt):
        move_amt = self.pace*dt
        while move_amt > 0: #allows us to, say, go down a tad and then go right on same dt
            if self.direction == Direction.DOWN:
                amount = min(self.background.distance_to_ladder_bottom((self.x, self.y)), move_amt) # can go down until you hit bottom of ladder
                self.move_down(amount)
                move_amt -=amount
                if self.background.distance_to_ladder_bottom((self.x, self.y)) == 0: # if we've hit bottom of ladder
                    self.direction = random.choice([Direction.RIGHT, Direction.LEFT])
            if self.background.above_ladder((self.x, self.y)) and self.direction == Direction.RIGHT or self.direction ==Direction.LEFT:
                if random.random() <.8: # Randomly doesn't  fly down
                    self.direction = Direction.DOWN
        self.update_position()      

        
    def on_resize(self, win_size):
        #TODO: This affects bird size, their current position, and rate/multiplier
        pass 
