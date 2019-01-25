"""
-------------------------------------------------------
[file name]
[program description]
-------------------------------------------------------
Author:  Konrad Gapinski
ID:     160713100
Email:   gapi3100@mylaurier.ca
__updated__ = "2019-01-22"
-------------------------------------------------------
"""
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class FloatingApp(App): 
    
    def build(self):
        return FloatLayout()
    
helloKivy = FloatingApp()

helloKivy.run()