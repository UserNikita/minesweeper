# -*- coding: utf-8 -*-
try:
    import Tkinter
except ModuleNotFoundError:
    import tkinter as Tkinter
from entities import Field, State, Colors


class Game(object):
    SCREEN_SIZE = 400
    COLS = 10
    CELL_SIZE = SCREEN_SIZE / COLS
    BOMBS_COUNT = 10

    game_over = False
    field = None

    def __init__(self, master):
        """Инициализация игры
        :param master: Tk - Объект главного окна
        """
        master.resizable(0, 0)  # Запрещаем ресайз окна

        # Создаём канвас
        self.canvas = Tkinter.Canvas(master, width=self.SCREEN_SIZE, height=self.SCREEN_SIZE)
        self.canvas.pack()

        # Добавляем обработчики для нажатий на клавиши мыши
        self.canvas.bind('<Button-1>', self.click_left_button)  # Левая клавиша
        self.canvas.bind('<Button-3>', self.click_right_button)  # Правая клавища

        # Добавление надписи с информацией о состоянии игры
        self.label = Tkinter.Label(master)
        self.label.pack()

        # Создание меню
        self.menu = Tkinter.Menu(master)
        self.menu.add_command(label="Начать заново", command=self.game_restart)
        master.config(menu=self.menu)  # Добавляем меню в окно приложения

        self.game_restart()

    def game_restart(self):
        """Метод сброса игровых данных на начальные"""
        self.game_over = False
        self.label.config(text="")
        self.field = Field(width=self.COLS, height=self.COLS)  # Создаём поле с заложенными минами
        self.field.plant_random_bombs(bombs=self.BOMBS_COUNT)
        print(self.field)
        self.draw_grid()  # Рисуем игровое поле

    def draw_grid(self):
        """Метод для отрисовки сетки"""
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.SCREEN_SIZE, self.SCREEN_SIZE, fill=Colors.CLOSED_CELL)
        for i in range(1, self.COLS):
            self.canvas.create_line(0, i * self.CELL_SIZE, self.SCREEN_SIZE, i * self.CELL_SIZE)
            self.canvas.create_line(i * self.CELL_SIZE, 0, i * self.CELL_SIZE, self.SCREEN_SIZE)

    def draw_bombs(self):
        """Метод отрисовки бомб на canvas"""
        for cell in self.field.get_cells_with_bombs():
            # Определить цвет ячейки
            cell_background = Colors.OPENED_CELL_WITH_BOMB if cell.state == State.OPEN else Colors.OPENED_CELL
            # Нарисовать открытую ячейку
            self.canvas.create_rectangle(cell.x * self.CELL_SIZE + 1, cell.y * self.CELL_SIZE + 1,
                                         cell.x * self.CELL_SIZE + self.CELL_SIZE,
                                         cell.y * self.CELL_SIZE + self.CELL_SIZE,
                                         fill=cell_background, width=0)
            # Нарисовать бомбу
            self.canvas.create_oval(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    fill=Colors.BOMB, width=1)
            self.canvas.create_line(cell.x * self.CELL_SIZE + self.CELL_SIZE / 2,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10,
                                    cell.x * self.CELL_SIZE + self.CELL_SIZE / 2,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 9,
                                    fill=Colors.BOMB, width=self.CELL_SIZE / 15)
            self.canvas.create_line(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 2,
                                    cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 9,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 2,
                                    fill=Colors.BOMB, width=self.CELL_SIZE / 15)
            self.canvas.create_line(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    fill=Colors.BOMB, width=self.CELL_SIZE / 15)
            self.canvas.create_line(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                    cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                    fill=Colors.BOMB, width=self.CELL_SIZE / 15)

    def draw_opened_cell(self, cell):
        """Метод отрисовки открытой ячейки
        :param cell: Cell - объект ячейки
        """
        # Рисуем пустую ячейку
        self.canvas.create_rectangle(cell.x * self.CELL_SIZE + 1,
                                     cell.y * self.CELL_SIZE + 1,
                                     cell.x * self.CELL_SIZE + self.CELL_SIZE,
                                     cell.y * self.CELL_SIZE + self.CELL_SIZE,
                                     fill=Colors.OPENED_CELL, width=0)
        if cell.value > 0:  # Если рядом с ячейкой лежит мина, то нарисовать значение ячейки
            self.canvas.create_text(int(cell.x * self.CELL_SIZE + self.CELL_SIZE / 2),
                                    int(cell.y * self.CELL_SIZE + self.CELL_SIZE / 2),
                                    text=str(cell.value), font=('Arial', int(self.CELL_SIZE / 2)))

    def draw_closed_cell(self, cell):
        """Метод отрисовки закрытой ячейки
        :param cell: Cell - объект ячейки
        """
        self.canvas.create_rectangle(cell.x * self.CELL_SIZE + 1, cell.y * self.CELL_SIZE + 1,
                                     cell.x * self.CELL_SIZE + self.CELL_SIZE, cell.y * self.CELL_SIZE + self.CELL_SIZE,
                                     fill=Colors.CLOSED_CELL, width=0)

    def draw_flag(self, cell):
        """Метод рисования флага в ячейке
        :param cell: Cell - объект ячейки
        """
        self.canvas.create_polygon(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                   cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 4,
                                   cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 7,
                                   cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                   cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 7,
                                   cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 6,
                                   fill=Colors.FLAG_POLYGON, outline=Colors.FLAG_POLYGON)
        self.canvas.create_line(cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 7,
                                cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 2,
                                cell.x * self.CELL_SIZE + self.CELL_SIZE / 10 * 7,
                                cell.y * self.CELL_SIZE + self.CELL_SIZE / 10 * 8,
                                fill=Colors.FLAG_LINE, width=self.CELL_SIZE / 20)

    def open_cell(self, x, y):
        """Рекурсивный метод открытия пустых ячеек
        :param x: int - координаты по X
        :param y: int - координаты по Y
        """
        cell = self.field.get_cell(x, y)
        cell.open()
        self.draw_opened_cell(cell)
        if cell.value == 0:  # Только если ячейка не находится рядом с бомбой
            for adjacent_cell in self.field.get_adjacent_closed_cells(x, y):
                self.open_cell(adjacent_cell.x, adjacent_cell.y)  # Рекурсивно открываем соседние ячейки

    def is_win(self):
        """Метод для проверки окончания игры.
        Игра считается успешно завершенной, если на всех оставшихся закрытых ячейках стоят флажки
        и в каждой находится мина.
        :return: bool - если игрок выиграл True, если игрок проиграл False
        """
        return all([c.has_flag() and c.has_bomb() for c in self.field.get_closed_cells()])

    def you_lose(self):
        """Метод вызывается, если игрок проиграл"""
        self.draw_bombs()
        self.label.config(text="Вы проиграли")
        self.game_over = True

    def you_win(self):
        """Метод вызывается, если игрок выиграл"""
        self.label.config(text="Вы выиграли")
        self.game_over = True

    def click_left_button(self, event):
        """Метод для обработки клавиши открытия ячейки.
        :param event: Объект события
        """
        if self.game_over:  # Если игра закончена, то нажатия клавишь не обрабатываются
            return

        x, y = int(event.x / self.CELL_SIZE), int(event.y / self.CELL_SIZE)  # Определить на какую ячейку кликнули
        self.open_cell(x, y)

        if self.field.get_cell(x, y).has_bomb():  # Если ячейка с бомбой, то игрок сразу проигрывает
            self.you_lose()
        elif self.is_win():  # Если ячейка была пустой, необходимо проверить победил игрок или нет
            self.you_win()

    def click_right_button(self, event):
        """Метод для обработки нажатия клавиши для установки или снятия флага
        В методе происходит проверка на то, что ячейка ещё закрыта. В открытые ячейки нельзя установить флаг.
        Если флаг установлен, то он снимается, но ячейка остаётся закрытой.
        :param event: Объект события
        """
        if self.game_over:  # Если игра закончена, то нажатия клавишь не обрабатываются
            return

        x, y = int(event.x / self.CELL_SIZE), int(event.y / self.CELL_SIZE)  # Определить на какую ячейку кликнули
        cell = self.field.get_cell(x, y)  # Из поля достать ячейку по координатам

        if cell.state is State.CLOSE:  # Если ячейка закрыта
            cell.set_flag()
            self.draw_flag(cell)  # Нарисовать флажок
            if self.is_win():  # Логика проверки на завершение игры
                self.you_win()
        elif cell.state is State.FLAG:  # Если на ячейке был установлен флажок
            cell.remove_flag()
            self.draw_closed_cell(cell)  # Нарисовать закрытую ячейку


def main():
    root = Tkinter.Tk()
    Game(root)
    root.mainloop()


if __name__ == '__main__':
    main()
