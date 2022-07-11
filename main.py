from kivy.app import App

from kivy.lang import Builder

from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock

from functools import partial

Builder.load_file("my.kv")


class Menu(Screen):
    pass


class field(Screen):
    ButtonLayout = 0
    selected_buttons = {}
    buttons = {}
    start_pos = 0
    end_pos = 0
    matrix = []
    queue = []
    using = set()
    is_false = 1
    way_not_searched = True

    DoneLayout = 0

    def init_buttons(self, ButtonLayout):
        field.ButtonLayout = ButtonLayout
        ButtonLayout.clear_widgets()
        for col in range(18):
            for row in range(32):
                field.buttons[(row, col)] = (Button(text=f'{row, col}', on_release=field.make_wall, opacity=0))
        for col in range(18):
            for row in range(32):
                ButtonLayout.add_widget(field.buttons[(row, col)])

    def make_wall(self):
        txt = tuple((int(self.text[1:-1].split()[0][:-1]), int(self.text[1:-1].split()[1])))
        if field.start_pos == 0:#len(field.selected_buttons) == 0 and not (txt in field.selected_buttons):
            self.background_color = (0, 128, 0)
            self.opacity = 1
            field.selected_buttons[txt] = self
            field.start_pos = txt
            self.color = (0, 128, 0)
        elif field.end_pos == 0:#len(field.selected_buttons) == 1 and not (txt in field.selected_buttons):
            self.background_color = (128, 0, 0)
            self.opacity = 1
            field.selected_buttons[txt] = self
            field.end_pos = txt
            self.color = (128, 0, 0)
        else:
            if not (txt in field.selected_buttons) and self.opacity == 0:
                self.background_color = (0, 0, 128)
                self.opacity = 1
                field.selected_buttons[txt] = self
                self.color = (0, 0, 128)
            elif txt != field.end_pos and txt != field.start_pos and self.background_color != [152, 255, 152, 1.0]:
                self.opacity = 0
                x,y = txt
                field.matrix[y+1][x+1] = 0
                field.selected_buttons.pop(txt)

    def Choose_Algorithm(self, DoneLayout = 0):
        if field.DoneLayout != 0:
            DoneLayout = field.DoneLayout
        DoneLayout.clear_widgets()
        DoneLayout.add_widget(Button(text='BFS', on_release=field.InitMatrixForSearch))
        DoneLayout.add_widget(Button(text='Dijkstra', on_release=field.InitMatrixForSearch))
        DoneLayout.add_widget(Button(text='Del all', on_release=field.DelAll))
        field.DoneLayout = DoneLayout

    def DelAll(self):
        field.way_not_searched = False #FIXME. Приходится нажимать 2 раза, т.к. поставлена задержка на вывод
        # за этим ещё тянется баг, из-за которого после нажатия на Del All можно словить момент и успеть нажать на BFS
        # после этого продолжится старый поиск пути в графе
        for elem in field.buttons.values():
            elem.opacity = 0
        field.selected_buttons = {}
        field.start_pos = 0
        field.end_pos = 0
        field.queue = []
        field.using = set()
        field.is_false = 1
        field.InitMatrixForSearch(self)
        field.DoneLayout.clear_widgets()
        field.DoneLayout.add_widget(Button(text = 'Choose start pos, then end pos, then walls, then press me', on_release = field.Choose_Algorithm))

    def InitMatrixForSearch(self):
        matrix = list(([0] * 34 for i in range(20)))
        st = field.start_pos
        nd = field.end_pos
        if st !=0 and nd != 0:
            field.way_not_searched = True
            matrix[st[1] + 1][st[0] + 1] = 1
            matrix[nd[1] + 1][nd[0] + 1] = 2
            st = (st[1] + 1, st[0] + 1)
            nd = (nd[1] + 1, nd[0] + 1)
            for y, x in field.selected_buttons.keys():
                if matrix[x + 1][y + 1] == 0:
                    matrix[x + 1][y + 1] = 3

            def Visualise_Delay(trash):
                Clock.schedule_once(partial(field.Search_And_Visualise, self, st, nd, matrix), field.is_false)
                if field.way_not_searched:
                    Clock.schedule_once(Visualise_Delay, field.is_false)
            Visualise_Delay(0)

    def Search_And_Visualise(self, st, nd, matrix, trash):
        using = field.using
        field.matrix = matrix
        for y, x in field.selected_buttons.keys():
            if matrix[x + 1][y + 1] == 0:
                matrix[x + 1][y + 1] = 3
        if self.text == 'BFS':
            if not(field.queue):
                field.queue = [(st, [])]
                queue = field.queue
                #print(st,nd)
            else:
                queue = field.queue
            if queue:
                (x, y), prd = queue.pop(0)
                if (x, y) == nd:
                    #print(prd)
                    #print(using)
                    field.way_not_searched = False
                    for elem in prd:
                        x,y = elem
                        field.buttons[(y - 1, x - 1)].background_color = (0, 255, 0)
                        field.buttons[(y - 1, x - 1)].opacity = 1
                        #field.buttons[(y - 1, x - 1)].text = ''
                if matrix[x][y] != 3 and 0 < x < 19 and 0 < y < 33 and (x, y) not in using:
                    queue += [((x + 1, y), prd + [(x, y)]), ((x, y + 1), prd + [(x, y)]), ((x - 1, y), prd + [(x, y)]),
                              ((x, y - 1), prd + [(x, y)])]
                    field.buttons[(y - 1, x - 1)].background_color = (152, 255, 152)
                    field.buttons[(y - 1, x - 1)].opacity = 1
                    #field.buttons[(y - 1, x - 1)].text = ''
                    matrix[x][y] = 6
                    using.add((x, y))
                    field.is_false = 0.1
                    #print(using)
                else: field.is_false = 0
        #for x in matrix:
        #    pass
        #    print(x)
        if self.text == 'JPS':
            pass


class app(App):
    screen = ScreenManager()

    def build(self):
        self.screen.add_widget(Menu(name='Menu'))
        self.screen.add_widget(field(name='field'))
        return self.screen


app().run()
"""
TODO LIST:
0.  done писец без ООП тяжко.. тут говнокод на говнокоде. Надо учить его, а потом переписывать
1.  done Сделать переход с главного экрана на экран выбора пути по кнопке 
2.  done Сделать рисовку пути 
3.  done Сделать поиск пути в графе
4.  done Сделать визуализацию поиска пути в графе
4.1 done Сделать ПЛАВНУЮ визуализацию поиска пути в графе
5. нет смысла, а жаль( Сделать нормальный ui в гм.
6. Сделать нормальный ui в рисовке
7. Всё в одном классе... это неудобно читать. Исправить!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
8. Приходится координаты писать в имени кнопки. Исправить.
9. Я узнал про декораторы. Применить.
10. Тут в логике провалы местами. Многие вещи лишний раз делаю и не очень красиво. Переделать.
"""
