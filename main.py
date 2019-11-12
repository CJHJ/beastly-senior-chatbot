# coding: utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
from kivy import resources

from chatbot import YugeChatBot

import sys
import os

# needed to build exe
import dbm

# set common variables
class commonVar:
    myicon = "icon.jpg"
    firstTime = True
    mainChat = YugeChatBot()
    end = False

class Chat(FloatLayout):
    # display the texts here
    def sentText(self, instance):

        print("inserted text!")
        s = str(self.a.text)
        s = s.replace('\n','')
        print(s)

        reply = ""

        if commonVar.firstTime:
            reply = commonVar.mainChat.startIntro(s)
            commonVar.firstTime = False
        elif commonVar.end:
            affirmative = ["はい","yes","YES","ok","オッケー","Yes","OK"]
            if s in affirmative:
                commonVar.end = False
                reply = commonVar.mainChat.startIntro(commonVar.mainChat.userName)
        else:
            commonVar.end,reply = commonVar.mainChat.getReply(s)

        # if String's length is not 0
        if len(s) != 0:
            # add images and Texts to gridlayout  as Image and Button
            # add speaker's talk
            self.wimg = Image(source = commonVar.myicon ,size_hint_x = 0.1)
            self.talk_button = Button(text = s ,font_name='TakaoPMincho.ttf',color = (0,0,0,1), size_hint_y = None,background_color = (255,255,255,255),text_size=[self.width*0.8, None])
            self.name_label = Label(text = commonVar.mainChat.userName , font_name='TakaoPMincho.ttf', size_hint_x = 0.1, font_size = 15, color = (0,0,0,1))
            self.empty_label = Label(text = "")

            self.container.add_widget(self.wimg)
            self.container.add_widget(self.talk_button)
            self.container.add_widget(self.name_label)
            self.container.add_widget(self.empty_label)

            # add 野獣先輩's talk
            self.wimg = Image(source='icon.jpg',size_hint_x = 0.1)
            self.talk_button = Button(text = reply ,font_name='TakaoPMincho.ttf',color = (0,0,0,1), size_hint_y = None,background_color = (255,255,255,255),text_size=[self.width*0.8, None])
            self.name_label = Label(text = "野獣先輩" , font_name='TakaoPMincho.ttf', size_hint_x = 0.1, font_size = 15, color = (0,0,0,1))
            self.empty_label = Label(text = "")

            self.container.add_widget(self.wimg)
            self.container.add_widget(self.talk_button)
            self.container.add_widget(self.name_label)
            self.container.add_widget(self.empty_label)

        if commonVar.end:
            # add 野獣先輩's talk
            self.wimg = Image(source='icon.jpg',size_hint_x = 0.1)
            self.talk_button = Button(text = "リスタート?" ,font_name='TakaoPMincho.ttf',color = (0,0,0,1), size_hint_y = None,background_color = (255,255,255,255),text_size=[self.width*0.8, None])
            self.name_label = Label(text = "野獣先輩" , font_name='TakaoPMincho.ttf', size_hint_x = 0.1, font_size = 15, color = (0,0,0,1))
            self.empty_label = Label(text = "")

            self.container.add_widget(self.wimg)
            self.container.add_widget(self.talk_button)
            self.container.add_widget(self.name_label)
            self.container.add_widget(self.empty_label)

    # just for debugging
    def reload(self):
        print("Inputbox reloaded")

class ChatApp(App):
    icon = 'icon.jpg'
    title = 'ChatBot'

    # # load setting file here
    def build_config(self, config):
        #設定用のファイルを使用(chat.ini)
        config.read('chat.ini')
        # load chat ini file
        self.red = float(config['section1']['red'])/255.0
        self.green = float(config['section1']['green'])/255.0
        self.blue = float(config['section1']['blue'])/255.0
        commonVar.myicon = str(config['section1']['topPicutre'])

    def build_settings(self, settings):
        #設定用のパネルを追加(settings_custom.json')
        settings.add_json_panel('Setting Panel', self.config, filename='settings_custom.json')

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        # chage the background color referes to the "chat.ini" file
        if section == "section1":
            if key == "red":
                self.red = float(value)/255.0
            if key == "green":
                self.green = float(value)/255.0
            if key == "blue":
                self.blue = float(value)/255.0
            # change top picture setting
            if key == "topPicutre":
                commonVar.myicon = str(value)

    def close_settings(self, settings):
        """
        The settings panel has been closed.
        """
        # update the BackGround's color
        self.changeBGColor()
        super(ChatApp, self).close_settings(settings)

    # change the background color
    def changeBGColor(self):
        print("---- chaged BGColor ----")
        Window.clearcolor = (self.red, self.green, self.blue, 1)

    def build(self):
        self.root = Builder.load_file('root.kv')
        Window.size = (400, 500)
        Window.clearcolor = (self.red, self.green, self.blue, 1)
        self.root = Chat()
        return self.root


if __name__ == '__main__':
    # resources.resource_add_path(resourcePath())
    ChatApp().run()
