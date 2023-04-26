import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import run
from imslib.screen import ScreenManager

from Serenade import MainScreen
from StartScreen import IntroScreen
from FinalSerenadeScreen import EndScreen

sm = ScreenManager()

sm.add_screen(IntroScreen(name='intro'))
sm.add_screen(MainScreen(name='main'))
sm.add_screen(EndScreen(name='end'))

run(sm)