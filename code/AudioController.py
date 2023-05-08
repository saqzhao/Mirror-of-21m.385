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
        self.mixer = Mixer()
        self.synth = Synth()
         # create TempoMap, AudioScheduler
        self.tempo_map  = SimpleTempoMap(120)
        self.sched = AudioScheduler(self.tempo_map)
        self.audio.set_generator(self.mixer)
        self.mixer.add(self.sched)
        self.sched.set_generator(self.synth)
        self.cmd = None
        self.vel = 80
        self.mixer.gain = 0.8

        # interval quiz
        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.base_pitch = 60
        self.channel = 0
        self.note_length = 150
        self.pause_between = 800

        #collectable
        self.pitch_idx = 0
        self.interval = []
        self.success = [0, 2, 5, 7]
        self.success_idx = 0
        self.victory_cmd = None
        self.collecting = False
        self.sfx_channel = 1

        #hit bird
        self.bird_track = WaveGenerator(WaveFile("../data/bird_sound.wav"))

        #program
        self.program = (0, 46)
        self.synth.program(self.channel, *self.program)
        self.synth.program(self.sfx_channel, *self.program)
    
        self.instruments = {'piano': (0, 0), 'violin': (8, 40), 'guitar': (8, 26)}


    def change_program(self, instrument_name):
        inst_prog = self.instruments[instrument_name]
        self.synth.program(self.channel, *inst_prog)
        self.synth.program(self.sfx_channel, *inst_prog)

    def hit_bird(self):
        self.bird_track.reset()
        self.mixer.add(self.bird_track)
        self.bird_track.play()
    
    def interval_quiz_success(self):
        self.collecting = True
        now = self.sched.get_tick()
        self.collect_sfx(now)

    def collect_instrument(self, instrument_name):
        if instrument_name == "violin":
            self.vel = 120
        else:
            self.vel = 60
        self.change_program(instrument_name)
        self.collecting = True
        now = self.sched.get_tick()
        self.collect_sfx(now)
    
    def stop_sfx(self, tick, pitch):
        self.synth.noteoff(self.sfx_channel, pitch)
    
    def collect_sfx(self, tick):
        if self.collecting:
            actual_pitch = 80 + self.success[self.success_idx]
            self.synth.noteon(self.sfx_channel, actual_pitch, self.vel)
            
            off_tick = tick + 60
            self.sched.post_at_tick(self.stop_sfx, off_tick, actual_pitch)
            self.success_idx += 1
            if self.success_idx < len(self.success):
                next_beat = tick + 60
                self.victory_cmd = self.sched.post_at_tick(self.collect_sfx, next_beat)
            else:
                self.collecting = False
                self.success_idx = 0


    def start(self):
        self.pitch_idx = 0
        now = self.sched.get_tick()
        next_beat = quantize_tick_up(now, self.note_length)
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat)

    def play_interval(self, interval): #called in intervalQuiz
        self.interval = [self.base_pitch, self.base_pitch + self.interval_midi[interval]]
        self.start()
    
    def _noteon(self, tick):
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