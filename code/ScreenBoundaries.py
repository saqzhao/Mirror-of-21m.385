import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy import metrics
from kivy.graphics import Color
from imslib.gfxutil import CRectangle

font_sz = metrics.dp(20)
button_side = metrics.dp(100)
button_sz = (button_side, button_side)

class ScreenBoundaries(Widget):
    def __init__(self):
        super(ScreenBoundaries, self).__init__()
        #horizontal
        self.canvas.add(Color(1, 0, 0, 1))
        self.canvas.add(CRectangle(csize = (Window.width, 5), cpos = (Window.width/2, Window.height)))
        self.canvas.add(Color(0, 1, 0, 1))
        self.canvas.add(CRectangle(csize = (Window.width, 5), cpos = (Window.width/2, 0)))
        self.canvas.add(Color(0, 0, 1, 1))
        self.canvas.add(CRectangle(csize = (Window.width, 5), cpos = (Window.width/2, Window.height/2)))

        #vertical
        self.canvas.add(Color(1, 0, 0, 1))
        self.canvas.add(CRectangle(csize = (5, Window.height), cpos = (0, Window.height/2)))
        self.canvas.add(Color(0, 1, 0, 1))
        self.canvas.add(CRectangle(csize = (5, Window.height), cpos = (Window.width, Window.height/2)))