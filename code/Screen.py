from imslib.screen import Screen

class MainScreenDisplay(Screen):
    '''
    class for the main game screen
    '''
    def __init__(self) -> None:
        super(MainScreenDisplay, self).__init__()
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