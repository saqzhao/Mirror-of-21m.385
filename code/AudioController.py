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
         # create TempoMap, AudioScheduler
        self.tempo_map  = SimpleTempoMap(120)
        self.sched = AudioScheduler(self.tempo_map)

        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)

        # interval quiz
        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.base_pitch = 60
        self.channel = 0
        self.vel = 80
        self.note_length = 150
        self.pause_between = 900
        self.program = (0, 46)
        self.synth.program(self.channel, *self.program)

    def play_interval(self, interval): #called in intervalQuiz
        self.synth.noteon(self.channel, self.base_pitch, self.vel)
        next_note = self.base_pitch + self.interval_midi[interval]

        now = self.sched.get_tick()
        first_noteoff = now+self.note_length
        second_noteon = first_noteoff + self.pause_between
        second_noteoff = second_noteon + self.note_length
        print(now, first_noteoff, second_noteon, second_noteoff)
        

        self.sched.post_at_tick(self._noteoff, first_noteoff, self.base_pitch)
        self.sched.post_at_tick(self._noteon, second_noteon, next_note)
        self.sched.post_at_tick(self._noteoff, second_noteoff, next_note)
        print('all posted')
    
    def _noteon(self, tick, pitch):
        print('noteon', pitch)
        self.synth.noteon(self.channel, pitch, self.vel)

    def _noteoff(self, tick, pitch):
        # just turn off the currently sounding note.
        print('noteoff', pitch)
        self.synth.noteoff(self.channel, pitch)

    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()