#####################################################################
#
# This software is to be used for MIT's class Interactive Music Systems only.
# Since this file may contain answers to homework problems, you MAY NOT release it publicly.
#
#####################################################################

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.audio import Audio
from imslib.synth import Synth
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile
from imslib.gfxutil import CEllipse, topleft_label, resize_topleft_label, CLabelRect, CRectangle

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image



# Scaling Constants we will be working with
belt_w =  0.8
border_w =  0.1 # each side of the belt
nowbar_h = 0.2
time_span = 2.0       # time (in seconds) that spans the full vertical height of the Window
time_to_nowbar = time_span * (1-nowbar_h)
slop_window = 0.1


class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        print("entering main widget")

        song_base_name = '../TakeMeOut'

        self.song_data  = SongData(song_base_name+"_gems.txt")
        self.audio_ctrl = AudioController(song_base_name)
        self.display    = GameDisplay(self.song_data)
        self.player = Player(self.song_data, self.audio_ctrl, self.display)

        self.canvas.add(self.display)

        self.info = topleft_label()
        self.add_widget(self.info)

        self.audio_ctrl.pause()


    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.audio_ctrl.toggle()

        # button down
        button_idx = lookup(keycode[1], 'asdfg', (0,1,2,3,4))
        if button_idx != None:
            self.player.on_button_down(button_idx+1)

    def on_key_up(self, keycode):
        # button up
        button_idx = lookup(keycode[1], 'asdfg', (0,1,2,3,4))
        if button_idx != None:
            self.player.on_button_up(button_idx+1)


    # handle changing displayed elements when window size changes
    # This function should call GameDisplay.on_resize
    def on_resize(self, win_size):
        resize_topleft_label(self.info)
        self.display.on_resize(win_size)
        #TODO : what else needs resizing ?

    def on_update(self):
        self.audio_ctrl.on_update()
        now = self.audio_ctrl.get_time()  # time of song in seconds.
        self.player.on_update(now)

        self.info.text = 'p: pause/unpause song\n'
        self.info.text += f'song time: {now:.2f}\n'
        # self.info.text += f'num objects: {self.display.get_num_object()}'


# Handles everything about Audio.
#   creates the main Audio object
#   load and plays solo and bg audio tracks
#   creates audio buffers for sound-fx (miss sound)
#   functions as the clock (returns song time elapsed)
class AudioController(object):
    def __init__(self, song_path):
        super(AudioController, self).__init__()
        self.audio = Audio(2)

        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        # song
        self.bg = WaveGenerator(WaveFile(song_path +"_bg"+ ".wav"))
        self.solo =WaveGenerator(WaveFile(song_path +"_solo"+ ".wav"))
        self.synth = Synth()
        self.synth.program(1, 128, 25) #0,120 128,16
        self.mixer.add(self.bg)
        self.mixer.add(self.solo)
        self.mixer.add(self.synth)



        # # start paused
        # self.track.pause()

    # start / stop the song
    def toggle(self):
        self.bg.play_toggle()
        self.solo.play_toggle()

    def pause(self):
        self.bg.pause()
        self.solo.pause()

    # mute / unmute the solo track
    def set_mute(self, mute): # True to mute, False for sound
        self.solo.gain = 0.0 if mute else 1.0

    # play a sound-fx (miss sound)
    def play_miss(self):
        print("miss sound!")
        self.synth.noteon(1, 50, 127) # channel, pitch, int(distance*velocity)
        pass

    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame

    # needed to update audio
    def on_update(self):
        self.audio.on_update()


# Holds data for gems and barlines.
class SongData(object):
    #Assumes our data looks something like TakeMeOut_data.txt where labels are 1-5 for lanes and 6 for barline
    def __init__(self, filepath):
        super(SongData, self).__init__()
        # self.gems_dict = {}  # Currently not in use because I think chronological use is better than non-ordered (?)
        self.gems = []# [(time, lane)]
        self.bars = [] # [time]
        self.gems_dict = dict()
        lines = self._lines_from_file(filepath)
        self._from_lines(lines)

    def get_gems(self):
        return self.gems

    def get_barlines(self):
        return self.bars

    def _lines_from_file(self, filename):
        x = []
        with open(filename) as f:
            for line in f:
                x.append(line)
        return x
  
    def _tokens_from_line(self, line):
        x= line.strip()
        return x.split("\t")

    def gem_from_index(self, index):
        return self.gems_dict[index]

    def _from_lines(self, lines):
        index = 0
        for line in lines:
            tokens = self._tokens_from_line(line) #[time, label]
            label = tokens[1] #label
            timeo = float(tokens[0])
            colors = [Color(rgb=(0,1,0)), Color(1,0,0), Color(1,1,0), Color(0,1,1), Color(rgb=(1,0,1))]
            if label == "6":
                self.bars.append( BarlineDisplay(timeo) )
            elif label in "12345":
                g = GemDisplay(int(label), timeo, colors[int(label)-1], index)
                self.gems.append(g)
                self.gems_dict[index]=g
                index +=1


def time_to_ypos(time, win_size):
    # TODO write this
    win_height = win_size[1]
    bottom =nowbar_h*win_height
    slope = (win_height)/time_span
    return bottom+time*slope

# Display for a single gem at a position with a hue or color
class GemDisplay(InstructionGroup):
    def __init__(self, lane, time, color, index):
        super(GemDisplay, self).__init__()
        self.index = index
        self.lane = lane
        self.time = time  # the timestamp (in seconds) of this beat in the song (ie, when does this beat occur?)
        self.color = color # color of this gem

        self.hit = False # Whether we've successfully hit the gem
        self.hittable = True # Whether we're still able to try and hit the gem

        self.hit_callback = lambda x : print(x, "no function here")
        self.pass_callback = lambda x : print(x, "no function here")
        self.win_size = (Window.width, Window.height)
        self.x_pos = border_w*self.win_size[0] + belt_w*self.win_size[0]/10*(lane*2-1)
        self.size = self.win_size[0]*belt_w/10
        self.gem = CEllipse(cpos = (self.x_pos, Window.height), size = (self.size, self.size), texture=Image('../gem2.png').texture) # line object to be drawn / animated in on_update()

        self.add(self.color)
        self.add(self.gem)

    # change to display this gem being hit
    def add_callback(self, callback, hit):
        if hit:
            self.hit_callback = callback
        else:
            self.pass_callback = callback

    def on_hit(self):
        if not self.hittable:
            print("This not should not have been hittable")
            return
        print("here")
        self.gem.texture=Image('../smiley.png').texture

        self.hit = True
        self.hittable = False
        self.hit_callback()

    # change to display a passed or missed gem
    def on_pass(self):
        self.pass_callback()
        self.hittable = False
        self.color.a = 0.5*self.color.a

    # this could also be just included in on_update, but that would do the math every time. This seems quicker
    def on_resize(self, win_size): 
        self.win_size = win_size
        self.x_pos = (self.lane*2-1)*belt_w*win_size[0]/10 + border_w*win_size[0] # actual position updates with on_update
        self.size = self.win_size[0]*belt_w/10
        self.gem.size = (self.size, self.size)

    # animate gem (position and animation) based on current time
    def on_update(self, now_time):
        if self.hit:
            self.size = self.size*0.8
            self.gem.size = (self.size, self.size)
        bottom= nowbar_h*self.win_size[0]
        y_pos=time_to_ypos(self.time-now_time, self.win_size)
        if not self.hit and self.hittable and now_time > self.time + slop_window:
            print(f"gem {self.index} passed")
            self.on_pass()
            # TODO: any sort of callback function we want here
            # TODO: SOUND CALLBACK
        self.gem.cpos = (self.x_pos, y_pos)
        if y_pos < -self.size: # wait for gem to completely leave screen
            return False
        return True

    def __str__(self):
        return f"GemDisplay object index {self.index}, lane {self.lane}, time {self.time}. Hittable? {self.hittable}"


# Displays a single barline on screen
class BarlineDisplay(InstructionGroup):
    def __init__(self, time):
        super(BarlineDisplay, self).__init__()
        self.belt_w = belt_w
        self.time = time  # the timestamp (in seconds) of this beat in the song (ie, when does this beat occur?)
        self.color = Color(hsv=(.1, .8, 1)) # color of this beat line
        self.line = Line(width = 3) # line object to be drawn / animated in on_update()
        self.add(self.color)
        self.add(self.line)
        self.win_size = (Window.width, Window.height)

    # animate barline (position) based on current time
    def on_update(self, now_time):
        y_pos=time_to_ypos(self.time-now_time, self.win_size)
        if y_pos < 0:
            return False
        self.line.points=((border_w*self.win_size[0], y_pos), ((belt_w+border_w)*self.win_size[0], y_pos))
        return True

    def on_resize(self, win_size):
        self.win_size = win_size


# Displays one button on the nowbar
class ButtonDisplay(InstructionGroup):
    def __init__(self, lane, color):
        super(ButtonDisplay, self).__init__()
        self.lane = lane
        self.color = color
        self.x = (lane*2-1)*belt_w*Window.width/10 + border_w*Window.width
        self.y = Window.height * nowbar_h
        self.add(self.color)
        self.size_o = Window.width*belt_w/10 #outer rim of circle
        self.size_i = self.size_o * 0.9 # inside filling of circle
        self.outer_circle = CEllipse(cpos=(self.x, self.y), size = (self.size_o, self.size_o))
        self.add(self.outer_circle)
        self.add(Color(rgb=(0,0,0)))
        self.inner_circle = CEllipse(cpos=(self.x, self.y), size = (self.size_i,self.size_i))
        self.add(self.inner_circle)
        self.add(self.color)
        

    # displays when button is pressed down
    def on_down(self):
        self.color.s = self.color.s/2 # TODO: Make sure this works. Should I just be changing the saturation? 
        self.inner_circle.size = (self.size_i *0.8, self.size_i*0.8)

    # back to normal state
    def on_up(self):
        self.color.s = self.color.s*2
        self.inner_circle.size = (self.size_i, self.size_i)

    # modify object positions based on new window size
    def on_resize(self, win_size):
        self.x = (self.lane*2-1)*belt_w*win_size[0]/10 + border_w*win_size[0]
        self.y = win_size[1] * nowbar_h
        self.size_o = win_size[0]*belt_w/10 
        self.size_i = self.size_o * 0.9 
        self.outer_circle.cpos = (self.x, self.y)
        self.inner_circle.cpos = (self.x, self.y)
        self.outer_circle.size = (self.size_o, self.size_o)
        self.inner_circle.size = (self.size_i, self.size_i)


# Displays all game elements: nowbar, buttons, barlines, gems
class GameDisplay(InstructionGroup):
    def __init__(self, song_data):
        super(GameDisplay, self).__init__()
        self.song_data = song_data
        self.buttons = []
        self.gems = song_data.get_gems()
        self.barlines = song_data.get_barlines()

        # Nowbar
        self.nowbar_height = nowbar_h*Window.height
        self.nowbar_margin = Window.width

        self.nowbar = Line(points=((self.nowbar_margin, self.nowbar_height), (Window.width-self.nowbar_margin, self.nowbar_height)))
        self.add(self.nowbar)

        # Buttons
        colors = [Color(rgb=(0,1,0)), Color(1,0,0), Color(1,1,0), Color(0,1,1), Color(rgb=(1,0,1))]
        for i in range(5):
            b =ButtonDisplay(i+1, colors[i])
            self.buttons.append(b)
            self.add(b)

        # Gems and Barline
        for gem in self.gems:
            self.add(gem)

        for bar in self.barlines: 
            self.add(bar)

        self.gem_idx = 0
        self.num_gems = len(self.gems)
        self.score = 0
        self.score_display= ScoreDisplay()
        self.add(self.score_display)

    # called by Player when succeeded in hitting this gem.
    def gem_hit(self, gem_idx):
        gem = self.gems[gem_idx]
        gem.on_hit()

    # called by Player on a miss 
    def gem_pass(self, gem_idx):
        gem = self.gems[gem_idx]
        gem.on_pass()

    # called by Player on button down
    def on_button_down(self, lane):
        # Visually change button 
        button = self.buttons[lane-1]
        button.on_down()

    # called by Player on button up
    def on_button_up(self, lane):
        # Visually change button
        button = self.buttons[lane-1]
        button.on_up()

    # called by Player to update score
    def set_score(self, score):
        self.score_display.set_score(score)

    def streak_update(self, current, longest):
        self.score_display.streak_update(current, longest)

    # for when the window size changes
    def on_resize(self, win_size):
        for button in self.buttons:
            button.on_resize(win_size)
        for gem in self.gems:
            gem.on_resize(win_size)
        for bar in self.barlines:
            bar.on_resize(win_size)

        self.score_display.on_resize(win_size)
        self.nowbar_height = nowbar_h*win_size[1]
        self.nowbar_margin = win_size[0]
        self.nowbar.points =((self.nowbar_margin, self.nowbar_height), (win_size[0]-self.nowbar_margin, self.nowbar_height))

    # call every frame to handle animation needs
    def on_update(self, now_time):
        # pass
        for i in range(self.gem_idx, self.num_gems): # assuming our gems are in chronological increasing order, slightly optimizes
            gem = self.gems[i]
            x = gem.on_update(now_time)
            if not x: 
                self.remove(gem)
                self.gem_idx+=1

        for bar in self.barlines:
            x= bar.on_update(now_time)
            if not x: 
                self.barlines.remove(bar)
                self.remove(bar)

class ScoreDisplay(InstructionGroup):
    def __init__(self):
        super(ScoreDisplay, self).__init__()
        self.score = 0
        self.current_streak = 0
        self.longest_streak = 0
        self.win_size = (Window.width, Window.height)
        self.pos = (self.win_size[0]*0.8, self.win_size[1]*0.9)
        self.display = CLabelRect(cpos=self.pos, text=f'Score: {self.score}\n Current Streak: {self.current_streak}\n Longest Streak: {self.longest_streak}', font_size=21)        # self.value = 
        # size = self.display.size
        # print(size)
        # self.background = CRectangle(cpos=self.pos)
        self.add(Color(rgb=(1,1,1)))
        # self.add(self.background)
        # self.add(Color(rgb = (0,0,0)))
        self.add(self.display)
        self.update_visual()
        print("made a score display")
        
    def on_resize(self, win_size):
        self.win_size = win_size
        self.pos = (self.win_size[0]*0.8, self.win_size[1]*0.8)
        self.display.cpos = self.pos
        # self.background.pos = self.pos

    def set_score(self, score):
        self.score = score
        self.update_visual()  

    def streak_update(self, current, longest):
        self.current_streak = current
        self.longest_streak = longest
        self.update_visual()      

    def update_visual(self):
        z =f'Score: {self.score}\n Current Streak: {self.current_streak}\n Longest Streak: {self.longest_streak}'
        print(z)
        self.display.set_text(z)
        pass

# Handles game logic and keeps track of score.
# Controls the GameDisplay and AudioCtrl based on what happens
class Player(object):
    def __init__(self, song_data, audio_ctrl, display):
        super(Player, self).__init__()
        self.song_data = song_data
        self.audio_ctrl = audio_ctrl
        self.display = display
        self.gems = self.song_data.get_gems()
        self.score = 0
        self.streak = 0
        self.longest_streak = 0

        for gem in self.gems:
            gem.add_callback(self.hit_callback, True)
            gem.add_callback(self.miss_callback, False)

    # called by MainWidget
    def on_button_down(self, lane):
        self.display.on_button_down(lane)
        hit = False
        miss_idxes = []
        now = self.audio_ctrl.get_time()
        for i in range(len(self.gems)):
            gem = self.gems[i]
            gem_lane = gem.lane
            time = gem.time
            if time > now +time_span:
                break
            if abs(time-now)<=slop_window and gem_lane == lane and gem.hittable: # Hit
                self.display.gem_hit(i)
                hit = True
            elif abs(time-now)<=slop_window: # Lane Missed this gem
                miss_idxes.append(i)
        if not hit and len(miss_idxes) >0: # Lane Miss
            for i in miss_idxes:
                print("Lane MISS")
                self.display.gem_pass(i) # sends indicies for each Lane Miss Gem
        elif not hit:
            print("temportal MISS")
            self.miss_callback()


    # called by MainWidget
    def on_button_up(self, lane):
        self.display.on_button_up(lane)

    # needed to check for pass gems (ie, went past the slop window)
    def on_update(self, time):
        self.display.on_update(time)

    def miss_callback(self):
        self.audio_ctrl.set_mute(True)
        self.audio_ctrl.play_miss()
        self.score = max(0, self.score-5)
        self.streak = 0
        self.display.set_score(self.score)
        self.display.streak_update(self.streak, self.longest_streak)

    def hit_callback(self):
        self.audio_ctrl.set_mute(False)
        self.score += 5
        self.display.set_score(self.score)
        self.streak +=1
        self.longest_streak = max(self.longest_streak, self.streak)
        self.display.streak_update(self.streak, self.longest_streak)



if __name__ == "__main__":
    run(MainWidget())
