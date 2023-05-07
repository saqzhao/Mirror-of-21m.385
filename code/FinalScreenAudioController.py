from imslib.audio import Audio
from imslib.synth import Synth
# from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile
from imslib.clock import Clock, SimpleTempoMap, Scheduler, AudioScheduler, tick_str, kTicksPerQuarter, quantize_tick_up

INSTRUMENT_MAPPINGS = {
    "violin": (0, 40),
    "piano": (0, 0),
    "guitar": (0, 27)
}

class Arpeggiator(object):
    def __init__(self, sched, synth, channel=0, program=(0, 40), callback = None):
        super(Arpeggiator, self).__init__()

        self.playing = False
        self.sched = sched
        self.audio = Audio(2)
        self.synth = synth
        self.audio.set_generator(self.synth)
        self.pitches = []
        self.pitch_index = 0
        self.note_len = 480
        self.articulation = 1
        self.channel = channel
        self.program = program
        self.callback = callback
        self.cmd = None

    def start(self):
        if self.playing:
            return
        self.pitch_index = 0
        self.playing = True
        self.synth.program(self.channel, self.program[0], self.program[1])
        now = self.sched.get_tick()
        next_beat = quantize_tick_up(now, self.note_len)
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat)

    def stop(self):
        if not self.playing:
            return
        self.playing = False
        if len(self.pitches) == 0:
            return
        if self.cmd is not None:
            self.sched.cancel(self.cmd)
            self.cmd = None
        pitch = self.pitches[self.pitch_index % len(self.pitches)]
        self.synth.noteoff(self.channel, pitch)

    def toggle(self):
        if self.playing:
            self.stop()
        else:
            self.start()

    def set_pitches(self, pitches):
        self.pitches = pitches

    def set_rhythm(self, length, articulation):
        self.note_len = length
        self.articulation = articulation

        if self.playing:
            self.sched.cancel(self.cmd)
            now = self.sched.get_tick()
            next_beat = quantize_tick_up(now, self.note_len)
            self.cmd = self.sched.post_at_tick(self._noteon, next_beat)

    def _noteon(self, tick):
        if not self.playing:
            return
        duration = self.note_len/self.articulation
        if len(self.pitches) == 0:
            return
        pitch = self.pitches[self.pitch_index % len(self.pitches)]
        self.pitch_index += 1
        self.synth.noteon(self.channel, pitch, 70)

        off_tick = tick + duration
        self.sched.post_at_tick(self._noteoff, off_tick, pitch)

        next_beat = tick + self.note_len
        self.cmd = self.sched.post_at_tick(self._noteon, next_beat)

    def _noteoff(self, tick, pitch):
        self.synth.noteoff(self.channel, pitch)

# Handles everything about Audio.
class FinalScreenAudioController(object):
    '''
    Handles: background music, collectible item collection sound, serenade at end of game,
             interval quiz audio
    '''
    def __init__(self):
        super(FinalScreenAudioController, self).__init__()
        self.audio = Audio(2)
        self.synth = Synth()

        self.tempo_map  = SimpleTempoMap(120)
        self.sched = AudioScheduler(self.tempo_map)

        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)

        self.instruments = set()
        self.arpeggiators = set()
        self.channels = {}
        self.playing_channel = 0

        self.interval_midi = {'2m': 1, '2M': 2, '3m': 3, '3M': 4, '4': 5, '5': 7, '6m': 8,
                             '6M': 9, '7m': 10, '7M': 11, '8': 12}
        self.pitches = [] 
        self.base_pitch = 60

    def on_instrument_collected(self, instrument):
        self.instruments.add(instrument)

    # start / stop the song
    def toggle(self):
        for arpeg in self.arpeggiators:
            arpeg.toggle()
    
    def add_instrument(self, instrument):
        this_arpeggiator = Arpeggiator(self.sched, self.synth, self.playing_channel, INSTRUMENT_MAPPINGS[instrument])
        this_arpeggiator.set_pitches(self.pitches)
        self.arpeggiators.add(this_arpeggiator)
        self.channels[instrument] = self.playing_channel
        self.playing_channel += 1

    def add_interval(self, interval):
        self.pitches.append(60)
        self.pitches.append(60+self.interval_midi[interval])

    def play_serenade(self):
        for instrument in self.instruments:
            self.add_instrument(instrument)
            
        self.playing_channel = 0

        for arpeg in self.arpeggiators:
            arpeg.toggle()

    # return current time (in seconds) of song
    def get_time(self):
        frame = self.bg.frame/Audio.sample_rate
        return frame
    
    # needed to update audio
    def on_update(self):
        self.audio.on_update()