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
    def __init__(self, background, pos ) -> None:
        super(Bird, self).__init__()
        self.background = background
        self.background.add(self) # Does this work?
        self.x=pos[0]
        self.y=pos[1]
        self.direction = Direction.RIGHT 
        self.active = False
        self.range = Window.width/10 # Distance that activates interval quiz
        self.pace = Window.width/4/5 # Position per time
        self.radius = Window.width/20
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
        # print(f"moving down {amount}")
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

    def on_update(self, dt):
        move_amt = self.pace*dt
        while move_amt > 0: #allows us to, say, go down a tad and then go right on same dt
            
            # Already going down
            if self.direction == Direction.DOWN: 
                amount = min(self.background.distance_to_ladder_bottom((self.x, self.y)), move_amt) # can go down until you hit bottom of ladder
                self.move_down(amount)
                move_amt -=amount
                if self.background.distance_to_ladder_bottom((self.x, self.y)) == 0: # if we've hit bottom of ladder
                    self.direction = random.choice([Direction.RIGHT, Direction.LEFT])
                    print("new direction: ", self.direction)
            # Can go down
            elif self.background.can_descend((self.x, self.y)) and self.direction == Direction.RIGHT or self.direction ==Direction.LEFT:
                if random.random() <.8: # Randomly doesn't  fly down
                    print("should be going down now")
                    self.direction = Direction.DOWN
                    self.move_down(move_amt)
                    break
                else:
                    print("not changing to down")
                    self.move_x(move_amt, self.direction)
                    move_amt = 0
            # Go to side
            else:
                self.move_x(move_amt, self.direction)
                move_amt = 0
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
