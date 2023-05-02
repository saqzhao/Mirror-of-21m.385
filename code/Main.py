import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import run
from imslib.screen import ScreenManager

from Serenade import MainScreen
from StartScreen import IntroScreen
from FinalSerenadeScreen import EndScreen
from TitleScreen import TitleScreen

sm = ScreenManager()
main = MainScreen(name='main')
sm.add_screen(TitleScreen(name='title'))
sm.add_screen(IntroScreen(name='intro', start_callback=main.start, interval_callback=main.select_intervals))
sm.add_screen(main)
sm.add_screen(EndScreen(name='end', main_screen=main))

run(sm)