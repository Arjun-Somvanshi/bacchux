from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import OptionProperty, ListProperty, StringProperty, NumericProperty
from kivy.metrics import sp, dp
from kivy.utils import platform
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
import os

Builder.load_string('''
#: import RGBA kivy.utils.rgba

<UIFilePicker>:
    canvas.before:
        Color: 
            rgba: root.background_color 
        Rectangle:
            size: self.size
            pos: self.pos

    title_bar_color: RGBA('#7057ff')
    background_color: RGBA('#ececec')
    lane_one_color: RGBA('#ececec')
    lane_two_color: RGBA('#b6b6b6')
    button_color_normal: RGBA('##7057ff')
    button_color_down: RGBA('#4b3caf')
    font_color_1: RGBA('#ececec')
    font_color_2: RGBA('#7057ff')
    directory_scroll_bar_color: RGBA('#7057ff')
    border_color: RGBA('#7057ff')
    path_label_color: RGBA('#7057ff')
    separator_color: RGBA('#b6b6b6')
    font_size_primary: sp(20)
    font_size_secondary: sp(15)

    orientation: 'vertical'
    spacing: dp(15)

    BoxLayout:
        id: title_bar
        canvas.before:
            Color: 
                rgba: root.title_bar_color 
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint_y: None
        height: dp(50)
        Label:
            halign: 'center'
            font_size: root.font_size_primary 
            color: root.font_color_1
            text: 'Files & Directories'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(15)
        BoxLayout:
            id: path_and_navigation_view
            spacing: dp(10)
            size_hint_y: None
            height: dp(40)
            Widget:
                size_hint_x: 0.1
            UIButton:
                background_color: root.button_color_normal if self.state == 'normal' else root.button_color_down
                text: 'Nav'
                size_hint_x: None
                width: self.texture_size[0] + dp(40)
            BoxLayout:
                id: path_view
                canvas.before:
                    Color:
                        rgba: root.border_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                    Color:
                        rgba: root.background_color
                    Rectangle:
                        size: self.width - root.pad, self.height - root.pad 
                        pos: self.x + root.pad/2, self.y + root.pad/2 
                spacing: dp(5)
                padding: dp(5)
                size_hint_max_x: root.path_view_max_width
            Widget:
                size_hint_x: 0.1

        Widget:

<DirectoryItem>:
    canvas.before:
        color:
            rgba: root.item_lane_color[0] if self.state == 'normal' else root.item_lane_color[1]
        Rectangle:
            size: self.size
            pos: self.pos
    spacing: dp(20)
    padding: dp(5)
    Iconwidget:
    Label:
        color: root.item_font_color
        font_size: root.item_font_size 

<IconWidget>:
    BoxLayout:

<PathLabel>:
    canvas.before:
        Color:
            rgba: root.backgroundColor
        Rectangle:
            size: self.size
            pos: self.pos
    color: root.fontColor
    font_size: root.fontSize
    shorten: True
    shorten_from: 'right'
    halign: 'center'
    text_size: self.width - dp(15), None
    size_hint_max_x: dp(200)

<UIButton@Button>:
    background_normal: ''
    background_down: ''
    
''')

class UIFilePicker(BoxLayout):
    default_paths = ListProperty([])
    current_path = StringProperty('')
    path_history = ListProperty([])
    mode = OptionProperty("file", options =["directory", "file"])
    title_bar_color = ListProperty([1,1,1,1])
    border_color = ListProperty([0,0,0,1])
    path_label_color = ListProperty([0,0,0,1])
    background_color = ListProperty([1,1,1,1])
    font_color_2 =  ListProperty([1,1,1,1])
    pad = NumericProperty(dp(4)) # for border padding 
    font_size_secondary = NumericProperty(sp(15)) # for border padding 

    path_view_max_width = NumericProperty(dp(600))
    
    def __init__(self,**kwargs):
        super(UIFilePicker, self).__init__(**kwargs)
        self.set_default_path()
        print(self.default_paths) # all the paths that should be readily available to the user
        self.load_home_dir()

    def load_home_dir(self):
        if platform in ['linux', 'win', 'macosx', 'ios']:
            home_path = self.default_paths[0][0]
            #home_path = "/home/zephyrus/kivy_projects"
            Clock.schedule_once(partial(self.update_path_view, home_path))
        elif platform == 'android':
            pass
        else:
            raise Exception("Unknown Platform")

    def update_path_view(self, path, *args):
        path_as_list = path.split(os.path.sep)[-5:]
        for directory in path_as_list:
            print("the directory is: ", directory)
            if not directory and platform == 'linux':
                directory = '/'
            directory_item = PathLabel(self.path_label_color, self.font_color_1, self.font_size_secondary)
            directory_item.text = directory
            self.ids.path_view.add_widget(directory_item)
            if directory != path_as_list[-1]:
                sep = PathLabel(self.separator_color, self.font_color_1, self.font_size_secondary) 
                sep.text = '>'
                sep.size_hint_x = None
                sep.width = dp(30)
                self.ids.path_view.add_widget(sep)
            self.path_view_max_width = len(path_as_list)*dp(200) + (len(path_as_list) - 1)*dp(30)
        print(self.ids.path_view.children)
            
    
    def set_default_path(self):
        '''This functions sets the default available paths for each os'''
        if platform == 'win':
            #user directory and related folders
            user_path = os.path.expanduser('~')
            self.default_paths.append(user_path, "Home")
            for folder in ["Desktop", "Documents", "Downloads", "Pictures", "Music", "Videos"]:
                self.default_paths.append((user_path+ os.path.sep +folder, folder))

            import win32api
            # getting the available drives 
            # or the available partitions in the file system
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:    
                self.default_paths.append((drive, drive[0]))
        
        elif platform == 'linux':
            self.default_paths.append((os.path.expanduser(u'~'), 'Home'))
            self.default_paths.append((os.path.sep, 'Root Directory'))
            self.default_paths.append((os.path.sep + u'mnt' + os.path.sep, os.path.sep + u'media'))
            username = self.default_paths[1][0].split(os.path.sep)[-1]
            media_mount_location = os.path.sep + u'run' + os.path.sep + u'media' + os.path.sep + username
            places = (os.path.sep + u'mnt' + os.path.sep, os.path.sep + u'media', media_mount_location)
            for place in places:
                if os.path.isdir(place):
                    for directory in next(os.walk(place))[1]:
                        self.default_paths.append((place + os.path.sep + directory + os.path.sep, directory))
        
        elif platform == 'macosx' or platform == 'ios':
            self.default_paths.append((os.path.expanduser(u'~') + os.path.sep, 'Home'))
            vol = os.path.sep + u'Volume'
            if os.path.isdir(vol):
                for drive in next(os.walk(vol))[1]:
                    self.default_paths.append((vol + os.path.sep + drive + os.path.sep, drive))            
        
        elif platform == 'android':
            paths = []
            paths.append(('/', "Root")) #root
            paths.append(('/storage', "Mounted Storage")) #root
            from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path
            app_path = app_storage_path()
            primary_external_path = primary_external_storage_path() 
            secondary_external_path = secondary_external_storage_path()
            if primary_external_path:
                paths.append((primary_external_path, "Internal Storage"))
            if secondary_external_path:
                paths.append((secondary_external_path, "External Storage"))
            for path in paths:
                realpath = os.path.realpath(path[0]) + os.path.sep
                if os.path.exists(realpath):
                    self.default_paths.append((realpath, path[1]))

class DirectoryItem(BoxLayout):
    item_lane_color = ListProperty([[0,0,0,0], [1,1,1,1]])
    item_font_color = ListProperty([1,1,1,1])
    item_font_size = NumericProperty(dp(18)) 

class PathLabel(Label):
    backgroundColor = ListProperty([0,0,0,1])
    fontColor = ListProperty([1,1,1,1])
    fontSize = NumericProperty(sp(14))
    def __init__(self, background_color, font_color, font_size, **kwargs):
        super(PathLabel, self).__init__(**kwargs)
        self.backgroundColor = background_color
        self.fontColor = font_color
        self.fontSize = font_size

class IconWidget(Widget):
    iconType = OptionProperty(['folder', ('folder', 'file')])
