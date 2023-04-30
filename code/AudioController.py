from imslib.audio import Audio
from imslib.synth import Synth
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile
from imslib.clock import Clock, SimpleTempoMap, AudioScheduler, tick_str, kTicksPerQuarter, quantize_tick_up


# Handles everything about Audio.
class AudioController(object):
    '''
    Handles: background music, collectible item collection sound, serenade at end of game,
             interval quiz audio
    '''
    def __init__(self):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.synth = Synth()
        self.audio.set_generator(self.synth)

        # create TempoMap, AudioScheduler
        self.tempo_map  = SimpleTempoMap(120)
        self.sched = AudioScheduler(self.tempo_map)

        # self.audio.set_generator(self.sched)

        # interval quiz
        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.base_pitch = 60
        self.channel = 0
        self.vel = 80
        self.note_length = 240
        self.pause_between = 480
        self.program = (0, 46)
        self.synth.program(self.channel, *self.program)

    def play_interval(self, interval): #called in intervalQuiz
        self.synth.noteon(self.channel, self.base_pitch, self.vel)
        next_note = self.base_pitch + self.interval_midi[interval]

        now = self.sched.get_tick()
        first_noteoff = now+self.note_length
        second_noteon = now+self.note_length+self.pause_between
        second_noteoff = now+2*self.note_length+self.pause_between
        print(now, first_noteoff,second_noteon, second_noteoff)
        self.sched.post_at_tick(self.synth.noteoff(self.channel, self.base_pitch), now+self.note_length)
        self.sched.post_at_tick(self.synth.noteon(self.channel, next_note, self.vel), now+self.note_length+self.pause_between)
        self.sched.post_at_tick(self.synth.noteoff(self.channel, next_note), now+2*self.note_length+self.pause_between)


    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()