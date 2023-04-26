import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.uix.widget import Widget

class QuizDisplay(Widget):
    def __init__(self):
        super(QuizDisplay, self).__init__()
        self.quiz = None
    
    def add_quiz(self, quiz):
        self.quiz = quiz
        self.add_widget(quiz)
    
    def remove_quiz(self):
        self.remove_widget(self.quiz)
        self.quiz = None
    
    def on_update(self, dt):
        if self.quiz:
            self.quiz.on_update(dt)