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

from background import BackgroundDisplay


# Scaling Constants we will be working with
ladder_w = 0.1
ramp_h = 0.75*ladder_w
player_h = 4*ramp_h


class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        pass #TODO

        # self.audio_ctrl
        # self.game_display
        # self.player
    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.audio_ctrl.toggle()

        # button down TODO: Change to arrow keys or controller controls
        button_idx = lookup(keycode[1], 'wasd', (0,1,2,3))
        if button_idx != None:
            self.player.on_button_down(button_idx+1)

    def on_key_up(self, keycode):
        # button up
        button_idx = lookup(keycode[1], 'wasd', (0,1,2,3))
        if button_idx != None:
            self.player.on_button_up(button_idx+1)


    # handle changing displayed elements when window size changes
    # This function should call GameDisplay.on_resize
    def on_resize(self, win_size):
        resize_topleft_label(self.info)
        self.display.on_resize(win_size)
        #TODO : anything else that needs resizing ?

    def on_update(self):
        self.audio_ctrl.on_update()
        now = self.audio_ctrl.get_time()  # time of song in seconds.
        # self.player.on_update(now)

        self.info.text = 'p: pause/unpause song\n'
        self.info.text += f'song time: {now:.2f}\n'
        # self.info.text += f'num objects: {self.display.get_num_object()}'

# Handles everything about Audio.
class AudioController(object):
    '''
    Handles: background music, collectible item collection sound, serenade at end of game,
             interval quiz audio
    '''
    def __init__(self):
        super(AudioController, self).__init__()
        self.audio = Audio(2)

        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)
        self.instruments = []

        # Add other variables here as needed
        # Maybe keep track of possible intervals to test? 

    # start / stop the song
    def toggle(self):
        #This may/may not work
        for instrument in self.instruments:
            instrument.toggle()

    def pause(self):
        #This may/may not work
        for instrument in self.instruments:
            instrument.pause()
    
    def add_instrument(self, program):
        # Program is tuple (a, b)
        new_synth = Synth()
        new_synth.program(.9, program[0], program[1])
        self.instruments.append(new_synth)
        self.mixer.add(new_synth)
        # TODO: make sure this works

    def play_serenade(self):
        pass #TODO

    def play_interval(self):
        pass #TODO

    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()

# Ladders, Floors, Player -- Basically whole game as we're playing it
class CharacterDisplay(InstructionGroup):
    '''
    Creates player character and controls movement
    '''
    def __init__(self) -> None:
        super(CharacterDisplay, self).__init__()
        self.background = BackgroundDisplay()
        # Ladders, Floors, Character??
    
    def on_button_down(self, button_value):
        pass #TODO

    def on_button_up(self, button_value):
        pass #TODO

    def can_climb(self, pos):
        # Returns True if player is on a ladder spot and can climb up
        return self.background.can_climb(pos)
    
    def can_descend(self, pos):
        # Returns True if a player is on a ladder spot and can climb down
        return self.background.can_descend(pos)

    def on_resize(self, win_size):
        pass #TODO

class StartScreenDisplay(InstructionGroup):
    '''

    '''
    def __init__(self) -> None:
        super(StartScreenDisplay, self).__init__()
        pass
    
    def on_button_down(self, button_value):
        pass #TODO

    def on_button_up(self, button_value):
        pass #TODO
    
    def start_game(self):
        # Returns True if player is on a ladder spot and can climb up
        pass #TODO

    def change_difficulty(self):
        pass #TODO

    def on_resize(self, win_size):
        pass #TODO

# # Switches between our possible screens (starting, settings, map/gameplay, serenade)
# # Forwards button presses to relevant smaller parts, callbacks to music settings if relevant
# class GameDisplay(InstructionGroup):
#     def __init__(self):
#         super(GameDisplay, self).__init__()
#         pass 

#     def on_button_right(self):
#         pass

#     def on_button_left(self):
#         pass

#     def on_button_down(self):
#         pass

#     def on_button_up(self):
#         pass

#     def on_resize(self, win_size):
#         pass

#     def on_update(self, now_time):
#         pass

class CollectedInstrumentDisplay(InstructionGroup):
    def __init__(self):
        super(CollectedInstrumentDisplay, self).__init__()
        pass #TODO
        
    def on_resize(self, win_size):
        pass #TODO

    def add_instrument(self, instrument):
        pass #TODO

class IntervalQuiz(InstructionGroup):
    def __init__(self):
        super(IntervalQuiz, self).__init__()
        pass #TODO
        
    def on_resize(self, win_size):
        pass #TODO

    def on_update(self, time):
        pass #TODO

class Player(object):
    '''
    Handles game logic
    Controls the GameDisplay and AudioCtrl based on what happens
    '''

    def __init__(self, audio_ctrl, display):
        super(Player, self).__init__()
        pass #TODO

    # called by MainWidget
    def on_button_down(self, button_value):
        pass #TODO

    # called by MainWidget
    def on_button_up(self, button_value):
        pass #TODO

    def on_update(self, time):
        # self.display.on_update(time)
        pass


if __name__ == "__main__":
    run(MainWidget())
