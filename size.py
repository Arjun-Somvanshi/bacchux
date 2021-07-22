from kivy.config import Config
Config.set('graphics', 'borderless', 1)
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
kv = '''
Widget:
'''
class SizeApp(App):
    def on_start(self):
        Window.maximize()
        Clock.schedule_once(self.document_size, 0.3)

    def document_size(self, dt):
        with open('resolution.txt', 'w') as f:
            f.write(str(Window.size[0]) + '\n' + str(Window.size[1]))
        self.stop()

    def build(self):
        return Builder.load_string(kv)

SizeApp().run()
