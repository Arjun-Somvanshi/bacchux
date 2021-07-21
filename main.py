from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import DictProperty, ListProperty, OptionProperty, StringProperty, BooleanProperty
from kivy.utils import rgba as RGBA
from kivy.uix.button import Button
import os

Window.size = (dp(400), dp(500))
app = None

class MenuScreen(Screen):
    def change_screen(self, screen_name):
        global app
        app.root.transition = SlideTransition(direction = 'left', duration = 0.35)
        app.root.current = screen_name

class ScheduleScreen(Screen):
    pass

class BackupDirectoriesScreen(Screen):
    directory_data = ListProperty([])

    def __init__(self, **kwargs):
        super(BackupDirectoriesScreen, self).__init__(**kwargs)
        for x in range(20):
            self.directory_data.append({'dir_name': 'hello' + str(x)})

class Directory(Button):
    dir_name = StringProperty('') 
    selected = BooleanProperty(False)
    path = StringProperty('')
    excludedPaths = ListProperty([])

class bacchuxApp(App):
    fonts = DictProperty({'logo': 'fonts/Expletus_Sans/ExpletusSans-BoldItalic.ttf', 
                          'regular': 'fonts/Open_Sans_Condensed/OpenSansCondensed-Bold.ttf'})

    theme = DictProperty({'button_normal': RGBA('#745C97'), 
                          'button_down': RGBA('#594774'),
                          'b1': RGBA('#39375B'),
                          'b2': RGBA('#D45079'),
                          'f1': RGBA('#D597CE'),
                          'f2': RGBA('#E9E1CC')
                        })
    position = OptionProperty('Right*Top', options=['Right*Top', 'Right*Bottom', 'Left*Top', 'Left*Bottom'])

    def on_start(self):
        if not os.path.isfile('resolution.txt'):
            import subprocess
            subprocess.run('python size.py', shell=True)
            Clock.schedule_once(self.read_resolution, 0.3)
        else:
            self.read_resolution(0)
        Window.clearcolor = self.theme['b1']

    def read_resolution(self, dt):
        with open('resolution.txt', 'r') as f:
            self.full_screen_size = f.readlines()
        Clock.schedule_once(self.position_window)

    def position_window(self, dt):
        if self.position == 'Right*Top':
            Window.left = float(self.full_screen_size[0])
            Window.top = 0
        elif self.position == 'Right*Bottom':
            Window.left = float(self.full_screen_size[0]) 
            Window.top = float(self.full_screen_size[1]) 
        elif self.position == 'Left*Top':
            Window.left = 0 
            Window.top = 0
        elif self.position == 'Left*Bottom':
            Window.left = 0 
            Window.top = float(self.full_screen_size[1]) 

        print('This is the window position: ', Window.left, Window.top)

    def build(self):
        global app
        app = self

if __name__ == '__main__':
    bacchuxApp().run()
