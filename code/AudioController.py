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

        print('hi')
        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)

        # interval quiz
        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.base_pitch = 60
        self.channel = 0
        self.vel = 80
        self.note_length = 150
        self.pause_between = 800
        self.program = (0, 46)
        self.synth.program(self.channel, *self.program)
        
        self.cmd = None
        self.pitch_idx = 0
        self.interval = []
    
        self.instruments = {'piano': (0, 0), 'violin': (0, 40), 'guitar': (0, 27)}

    def change_program(self, instrument_name):
        inst_prog = self.instruments[instrument_name]
        self.synth.program(self.channel, *inst_prog)

    def start(self):
        self.pitch_idx = 0
        now = self.sched.get_tick()
        next_beat = quantize_tick_up(now, self.note_length)
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat)
        print('started')

    def play_interval(self, interval): #called in intervalQuiz
        self.interval = [self.base_pitch, self.base_pitch + self.interval_midi[interval]]
        self.start()
    
    def _noteon(self, tick):
        print('noteon')
        duration = 150
        pitch_idx = self.pitch_idx % 2
        pitch = self.interval[pitch_idx]
        self.pitch_idx += 1
        self.synth.noteon(self.channel, pitch, self.vel)

        off_tick = tick + duration
        self.sched.post_at_tick(self._noteoff, off_tick, pitch)

        next_beat = tick + self.pause_between
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat)

    def _noteoff(self, tick, pitch):
        # just turn off the currently sounding note.
        print('noteoff', pitch)
        self.synth.noteoff(self.channel, pitch)
    
    def stop(self):
        if self.cmd is not None:
            self.sched.cancel(self.cmd)
            self.cmd = None
        pitch_idx = self.pitch_idx % 2
        pitch = self.interval[pitch_idx]
        self.synth.noteoff(self.channel, pitch)

    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()