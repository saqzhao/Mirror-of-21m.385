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