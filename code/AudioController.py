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

        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)
        self.audio.set_generator(self.mixer)

        # interval quiz
        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.base_pitch = 60
        self.quiz_channel = 0
        self.vel = 80
        self.note_length = 90

        # collectibles
        self.instruments = []

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

    # from ps4
    def _noteoff(self, tick, pitch):
        # just turn off the currently sounding note.
        self.synth.noteoff(self.channel, pitch)

    def play_interval(self, interval): #called in intervalQuiz
        self.synth.noteon(self.quiz_channel, self.base_pitch, self.vel)
        next_note = self.base_pitch + self.interval_midi[interval]

        now = self.sched.get_tick()
        next_beat = quantize_tick_up(now, self.note_length)

        self.sched.post_at_tick(self._noteoff, next_beat, self.base_pitch)
        self.cmd = self.sched.post_at_tick(self.synth.noteon(self.quiz_channel, next_note, self.vel), next_beat)

        interval_off = quantize_tick_up(now, 2*self.note_length)
        self.sched.post_at_tick(self._noteoff, interval_off, next_note)


    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()