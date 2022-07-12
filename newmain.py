from kivy.app import App

from kivy.lang import Builder

from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock

from functools import partial

Builder.load_file("my.kv")


class Menu(Screen):
    pass


class Field(Screen):
    def choose_algorithm(self):
        DoneLayout


class DoneLayout():
