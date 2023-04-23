from imslib.audio import Audio
from imslib.synth import Synth
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile
from imslib.clock import Clock, SimpleTempoMap, AudioScheduler, tick_str, kTicksPerQuarter, quantize_tick_up

INSTRUMENT_MAPPINGS = {
    "violin": (0, 40),
    "piano": (0, 0),
    "guitar": (0, 27)
}

DUMMY_SEQUENCE = (60, 61, 62, 63, 64, 65)

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
        self.instruments = set()
        self.synths = set()
        self.i = 0
        self.channels = {}
        self.playing_channel = 0
        self.notelen = 2

    def on_instrument_collected(self, instrument):
        self.instruments.add(instrument)

    # start / stop the song
    def toggle(self):
        #This may/may not work
        for synth in self.synths:
            synth.toggle()

    def pause(self):
        #This may/may not work
        for synth in self.synths:
            synth.pause()
    
    def add_instrument(self, program):
        # Program is tuple (a, b)
        new_synth = Synth()
        new_synth.program(self.playing_channel, program[0], program[1])
        self.synths.add(new_synth)
        self.channels[new_synth] = self.playing_channel
        self.playing_channel += 1
        self.mixer.add(new_synth)
        # TODO: make sure this works

    def play_serenade(self):
        self.i = 0
        for instrument in self.instruments:
            self.add_instrument(INSTRUMENT_MAPPINGS[instrument])

        # now = self.sched.get_tick()
        # next_beat = quantize_tick_up(now, 480)
        for synth in self.synths:
            print(self.sched.get_tick())
            self._noteon(self.sched.get_tick(), (synth, DUMMY_SEQUENCE[self.i]))
        
        self.playing_channel = 0

    def _noteon(self, tick, synth_pitch):
        synth, pitch = synth_pitch
        synth.noteon(self.channels[synth], pitch, self.vel)
        off_tick = tick + self.notelen #TODO(ashleymg): debug why note off isn't happening and next note_on isn't getting called
        print(off_tick)
        self.sched.post_at_tick(self._synth_noteoff, off_tick, (synth, pitch, self.channels[synth]))
        self.i += 1
        next_beat = tick + self.notelen
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat, (synth, DUMMY_SEQUENCE[self.i+1]))

    def _synth_noteoff(self, tick, synth_pitch_channel):
        synth, pitch, channel = synth_pitch_channel
        synth.noteoff(channel, pitch)
        print("102")

    def _noteoff(self, tick, pitch):
        self.synth.noteoff(self.quiz_channel, pitch)

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