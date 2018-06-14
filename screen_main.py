import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from comments3 import run_this
#from entercomment1 import delete_com
from kivy.uix.screenmanager import Screen, ScreenManager
import pandas as pd
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from rejected import reject_com
from algo import hamOrSpam
from kivy import Config
Config.set('graphics', 'multisamples', '0')

class LinkLayout(FloatLayout):
    pass

class MainScreen(Screen):
    def build(self):
        return LinkLayout()

    #def ig_print(self):
    #    do_print()

    def retrieve_comments(self, video_link):
        print('ok')
        vid_id = video_link
        vid_id = vid_id.split('?v=')
        print(vid_id[1])
        run_this(vid_id[1])
        hamOrSpam()
		#comment_list()


class ToggleButton(ToggleButton):
    pass

class Scroll5():
    pass


class AnotherScreen(Screen):

    global normal_list
    normal_list = []

    def normal_buttons(self, obj):
        print(normal_list)

    def on_state(self, togglebutton):
        tb = togglebutton
        print(tb, tb.state, tb.id)
        if tb.state == 'normal':
            normal_list.append(int(tb.id))
        if tb.state == 'down':
            normal_list.remove(int(tb.id))

    def buildidk(self):
        #super(AnotherScreen, self).build()
        #container = self.root.ids.container
        df = pd.read_csv(r"spam_comments.csv", encoding='latin-1')
        container = self.ids.container
        for i in range(len(df)):
            container.add_widget(ToggleButton(text=df.comment[i], state='down', id=str(i), on_press=self.normal_buttons))
        #return self.root
    def delete_comments(self):
        delete_list = normal_list[::2]
        df = pd.read_csv(r"spam_comments.csv", encoding='latin-1')
        df = df.drop(df.index[delete_list])
        reject_com(df.id.tolist())

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file('Scroll9.kv')

class Scroll9App(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    Scroll9App().run()