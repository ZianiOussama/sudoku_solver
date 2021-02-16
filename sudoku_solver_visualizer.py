import threading
import time

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.app import MDApp

Window.size = (630, 630)


class Cell(Label):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)


class Block(GridLayout):
    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 2
        [self.add_widget(Cell()) for _ in range(9)]


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 4
        [self.add_widget(Block()) for _ in range(9)]
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.current = None

    def on_touch_down(self, touch):
        x, y = touch.pos
        for block in self.children:
            for cell in block.children:
                cell.bg_color = [1, 1, 1, 1]
                if cell.collide_point(x, y):
                    cell.bg_color = [.9, .9, 1, 0.95]
                    self.current = cell

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        try:
            num = int(text)
            if num:
                self.previous = self.current.text
                self.current.text = str(num)
        except:
            if keycode[1] == 'backspace':
                self.current.text = ''
            if keycode[1] == 'enter':
                self.start_threading(self.solve)
            if keycode[1] == 'spacebar':
                self.clear_widgets()
                [self.add_widget(Block()) for _ in range(9)]

        try:
            self.current.color = [0, 0, 0, .7]
            self.check(self.current)
        except:pass

        if keycode[1] == 'escape':
            keyboard.release()
        return True

    def check(self, current):
        for block in self.children:
            for cell in block.children:

                if current in block.children and cell.text:
                    if cell.text == current.text and cell != current:
                        self.set_to_red(cell, current)
                    if cell.text == self.previous != current.text:
                        self.reset_colors(cell, current)
                        self.check(cell)

                if cell.center_x == current.center_x and cell.text:
                    if cell.text == current.text and cell != current:
                        self.set_to_red(cell, current)
                    if cell.text == self.previous != current.text:
                        self.reset_colors(cell, current)
                        self.check(cell)

                if cell.center_y == current.center_y and cell.text:
                    if cell.text == current.text and cell != current:
                        self.set_to_red(cell, current)
                    if cell.text == self.previous != current.text:
                        self.reset_colors(cell, current)
                        self.check(cell)

    def set_to_red(self, cell, current):
        cell.color = [1, 0, 0, 1]
        current.color = [1, 0, 0, 1]
        cell.bg_color = [274 / 255, 207 / 255, 214 / 255, 1]
        current.bg_color = [274 / 255, 207 / 255, 214 / 255, 1]

    def reset_colors(self, cell, current):
        cell.color = [0, 0, 0, .7]
        cell.bg_color = [1, 1, 1, 1]

    def solve(self):
        for block in self.children:
            for cell in block.children:
                if not cell.text:
                    time.sleep(1 / 30)
                    for i in range(1, 10):
                        cell.text = str(i)
                        if not self.is_possible(cell):
                            cell.text = ''
                            continue
                        self.solve()
                        cell.text = ''

                    return
        a = 0
        for block in self.children:
            for cell in block.children:
                a += 1
                print(str(a)+'>', cell.text)

        input('>>>> ')

    def start_threading(self, func):
        t1 = threading.Thread(target=func)
        t2 = threading.Thread(target=self.clock)

        t1.start()
        t2.start()

    def clock(self):
        Clock.schedule_interval(self.update_grid, 1 / 1000)

    def update_grid(self, dt):
        for block in self.children:
            for cell in block.children:
                pass

    def is_possible(self, current):
        for block in self.children:
            for cell in block.children:

                if current in block.children:
                    if cell.text == current.text and cell != current:
                        return False

                if cell.center_x == current.center_x:
                    if cell.text == current.text and cell != current:
                        return False

                if cell.center_y == current.center_y:
                    if cell.text == current.text and cell != current:
                        return False
        return True


class Sudoku(MDApp):
    theme_cls = 'Dark'

    def build(self):
        return Grid()


if __name__ == '__main__':
    sd = Sudoku()
    sd.run()
