from kivy.app import App

from kivy.lang import Builder

from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock

from functools import partial

from kivy.core.window import Window


Builder.load_file("my.kv")


class NewButton(Button):
    cords = (0, 0)


class Menu(Screen):
    pass


class Field(Screen):
    window_size = Window.size
    selected_buttons = {}
    buttons = {}
    start_pos = ()
    end_pos = ()
    matrix = list(([0] * (Window.size[0]//100+2) for _ in range(Window.size[1]//100+2)))
    queue = []
    using = set()
    is_false = 1
    way_not_searched = 2

    @staticmethod
    def add_search_buttons(done_layout):
        done_layout.clear_widgets()
        done_layout.add_widget(Button(text='BFS', on_release=Field.init_matrix_for_search))
        done_layout.add_widget(Button(text='Del all', on_release=Field.del_all))

    @staticmethod
    def init_buttons(button_layout):
        button_layout.clear_widgets()
        for col in range(Window.size[1]//100):
            for row in range(Window.size[0]//100):
                Field.buttons[(row, col)] = (NewButton(on_release=Field.make_wall, opacity=0))
                Field.buttons[(row, col)].cords = (row, col)
                button_layout.add_widget(Field.buttons[(row, col)])

    def make_wall(self):
        if not Field.start_pos:
            self.background_color = (0, 128, 0)
            self.opacity = 1
            Field.selected_buttons[self.cords] = self
            Field.start_pos = self.cords
            self.color = (0, 128, 0)
        elif not Field.end_pos and self.cords != Field.start_pos:
            self.background_color = (128, 0, 0)
            self.opacity = 1
            Field.selected_buttons[self.cords] = self
            Field.end_pos = self.cords
            self.color = (128, 0, 0)
        else:
            if self.cords not in Field.selected_buttons and self.opacity == 0:
                self.background_color = (0, 0, 128)
                self.opacity = 1
                Field.selected_buttons[self.cords] = self
                self.color = (0, 0, 128)
            elif self.cords != Field.end_pos and self.cords != Field.start_pos and self.cords in Field.selected_buttons:
                self.opacity = 0
                x,y = self.cords
                Field.matrix[y+1][x+1] = 0
                Field.selected_buttons.pop(self.cords)

    def del_all(self):
        if Field.way_not_searched != 0:
            Field.way_not_searched -= 1
        for elem in Field.buttons.values():
            elem.opacity = 0
        Field.selected_buttons = {}
        Field.start_pos = 0
        Field.end_pos = 0
        Field.queue = []
        Field.using = set()
        Field.matrix = list(([0] * (Window.size[0]//100+2) for _ in range(Window.size[1]//100+2)))
        if Field.way_not_searched:
            Clock.schedule_once(partial(Field.del_all), 0.4)

    @staticmethod
    def init_matrix_for_search(self):
        matrix = list(([0] * (Window.size[0]//100+2) for _ in range(Window.size[1]//100+2)))
        st = Field.start_pos
        nd = Field.end_pos
        if st != 0 and nd != 0:
            Field.way_not_searched = 2
            matrix[st[1] + 1][st[0] + 1] = 1
            matrix[nd[1] + 1][nd[0] + 1] = 2
            st = (st[1] + 1, st[0] + 1)
            nd = (nd[1] + 1, nd[0] + 1)
            for y, x in Field.selected_buttons.keys():
                if matrix[x + 1][y + 1] == 0:
                    matrix[x + 1][y + 1] = 3

            def visualise_delay(trash):
                Clock.schedule_once(partial(Field.search_and_visualise, self, st, nd, matrix), Field.is_false)
                if Field.way_not_searched == 2:
                    Clock.schedule_once(visualise_delay, Field.is_false)
            visualise_delay(0)

    def search_and_visualise(self, st, nd, matrix, trash):
        using = Field.using
        Field.matrix = matrix
        for y, x in Field.selected_buttons.keys():
            if matrix[x + 1][y + 1] == 0:
                matrix[x + 1][y + 1] = 3
        if self.text == 'BFS':
            if not Field.queue:
                Field.queue = [(st, [])]
                queue = Field.queue
            else:
                queue = Field.queue
            if queue:
                (x, y), prd = queue.pop(0)
                if (x, y) == nd:
                    Field.way_not_searched = 0
                    for elem in prd:
                        x, y = elem
                        Field.buttons[(y - 1, x - 1)].background_color = (0, 255, 0)
                        Field.buttons[(y - 1, x - 1)].opacity = 1
                if matrix[x][y] != 3 and 0 < x < Window.size[1]//100+1 and 0 < y < Window.size[0]//100+1 \
                        and (x, y) not in using:
                    queue += [((x + 1, y), prd + [(x, y)]), ((x, y + 1), prd + [(x, y)]), ((x - 1, y), prd + [(x, y)]),
                              ((x, y - 1), prd + [(x, y)])]
                    Field.buttons[(y - 1, x - 1)].background_color = (152, 255, 152)
                    Field.buttons[(y - 1, x - 1)].opacity = 1
                    matrix[x][y] = 6
                    using.add((x, y))
                    Field.is_false = 0.1
                else:
                    Field.is_false = 0


class MyApp(App):
    screen = ScreenManager()

    def build(self):
        self.screen.add_widget(Menu(name='Menu'))
        self.screen.add_widget(Field(name='Field'))
        return self.screen


MyApp().run()

"""
TODO LIST:
Сделать норм кнопки и норм UI
"""
