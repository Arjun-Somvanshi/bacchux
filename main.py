from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import DictProperty, ListProperty, OptionProperty
from kivy.utils import rgba as RGBA
Window.size = (dp(400), dp(500))
Window.clearcolor = RGBA('#D45079')

class MenuScreen(Screen):
    pass

class ScheduleScreen(Screen):
    pass

class BackupDirectoriesScreen(Screen):
    pass

class bacchuxApp(App):
    fonts = DictProperty({'logo': 'fonts/Expletus_Sans/ExpletusSans-BoldItalic.ttf', 
                          'regular': 'fonts/Open_Sans_Condensed/OpenSansCondensed-Light.ttf'})

    theme = DictProperty({'button_normal': (1,1,1,1), 
                          'button_down': (1,1,1,1),
                          'b1': RGBA('#6E5773'),
                          'b2': RGBA('#D45079'),
                          'f1': RGBA('#EA9085'),
                          'f2': RGBA('#E9E1CC')
                        })
    position = OptionProperty('Right*Top', options=['Right*Top', 'Right*Bottom', 'Left*Top', 'Left*Bottom'])

    def on_start(self):
        import subprocess
        subprocess.run('python size.py', shell=True)
        Clock.schedule_once(self.read_resolution, 0.3)

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
        pass

if __name__ == '__main__':
    bacchuxApp().run()
