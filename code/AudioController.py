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