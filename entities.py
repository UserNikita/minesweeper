# -*- coding: utf-8 -*-
"""Объекты игры - ячейка, поле"""
import random


class Colors(object):
    """Класс с цветами объектов"""
    BOMB = '#000000'
    CLOSED_CELL = '#6ab04c'
    OPENED_CELL = '#badc58'
    OPENED_CELL_WITH_BOMB = '#ff5722'
    FLAG_POLYGON = '#d35400'
    FLAG_LINE = '#000000'


class State(object):
    """Класс состояний ячейки"""
    CLOSE = 0
    OPEN = 1
    FLAG = 2


class Cell(object):
    """Класс ячейки игрового поля"""

    def __init__(self, x, y):
        """Инициализация ячейки
        :param x: int - координата ячейки по оси X
        :param y: int - координата ячейки по оси Y
        """
        self.x = x
        self.y = y
        self.value = 0  # Значение показывает количетсво бомб по соседству. -1 означает, что в ячейке бомба
        self.state = State.CLOSE  # Состояние ячейки (закрыта, открыта, помечена флагом)

    def has_bomb(self):
        """Метод для проверки наличия бомбы в ячейке
        Возвращает True если ячейка содержит бомбу, иначе False
        :return: bool
        """
        return self.value == -1

    def plant_bomb(self):
        """Метод для закладки бомбы в ячейку"""
        self.value = -1

    def has_flag(self):
        """Проверка на наличие флага
        :return: bool - True если флаг установлен, иначе False
        """
        return self.state == State.FLAG

    def set_flag(self):
        """Установить флаг"""
        self.state = State.FLAG

    def remove_flag(self):
        """Снять флаг"""
        self.state = State.CLOSE

    def open(self):
        """Открыть ячейку"""
        self.state = State.OPEN

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Cell x={} y={}>".format(self.x, self.y)


class Field(object):
    def __init__(self, width=10, height=10):
        """Метод инициализации игрового поля
        :param width: int - ширина поля
        :param height: int - высота поля
        """
        self.width = width
        self.height = height
        # Список ячеек поля
        self._cell_list = [Cell(x=n % self.width, y=int(n / self.width)) for n in range(self.height * self.width)]

    def __str__(self):
        s = '  ' + ''.join([str(n) for n in range(self.width)]) + '\n'
        for y in range(self.height):
            s += str(y) + ' '
            for x in range(self.width):
                s += 'x' if self.get_cell(x, y).has_bomb() else str(self.get_cell(x, y).value)
            s += '\n'
        return s

    def get_cell(self, x, y):
        """Получить ячейку по координатам
        :param x: int - координата ячейки по X
        :param y: int - координата ячейки по Y
        :return: Cell - объект ячейки или None
        """
        assert x >= 0, "X должен быть больше или равен 0"
        assert y >= 0, "Y должен быть больше или равен 0"
        assert x < self.width, "X должен быть меньше %s" % self.width
        assert y < self.height, "Y должен быть меньше %s" % self.height
        return self._cell_list[y * self.width + x]

    def get_copy_cells_list(self):
        """Метод для получения копии списка всех ячеек
        :return: list of Cell - копия списка с объектами ячеек
        """
        return self._cell_list[:]

    def get_adjacent_cells(self, x, y):
        """Метод для получения соседних ячеек
        :param x: int - координата по X
        :param y: int - координата по Y
        :return: list of Cell - список из объектов ячеек
        """
        # Подготовить список из кортежей с координатами соседних ячеек
        cells_coordinates = [{'y': j, 'x': i} for j in range(y - 1, y + 2) for i in range(x - 1, x + 2)]
        # Убрать то, что находится за пределами игрового поля
        cells_coordinates = filter(
            lambda c: (self.height > c['x'] >= 0) and (self.width > c['y'] >= 0),
            cells_coordinates)
        # Убрать саму ячейку для которой найдены смежные ячейки
        cells_coordinates = filter(
            lambda c: not (c['x'] == x and c['y'] == y),
            cells_coordinates)
        cells = [self.get_cell(**coordinates) for coordinates in cells_coordinates]
        return cells

    def get_adjacent_closed_cells(self, x, y):
        """Метод получения соседних закрытых ячеек
        :param x: int - координата x
        :param y: int - координата y
        :return: list of Cell - список из объектов класса ячейки
        """
        cells = filter(lambda c: c.state is State.CLOSE, self.get_adjacent_cells(x, y))
        return cells

    def get_cells_with_bombs(self):
        """Получение ячеек с бомбами
        :return: list of Cell - список с объектами ячеек
        """
        cells_with_bombs = filter(lambda c: c.has_bomb(), self._cell_list)
        return cells_with_bombs

    def get_closed_cells(self):
        """Получение закрытых ячеек
        :return: list of Cell - список с объектами ячеек
        """
        closed_cells = filter(lambda c: c.state != State.OPEN, self._cell_list)
        return closed_cells

    def plant_random_bombs(self, bombs=10, seed=None):
        """Метод для закладки мин в поле"""
        if seed:  # Установка числа для инициализации случайных последовательностей
            random.seed(seed)  # Необходимо для тестирования метода
        cells = self.get_copy_cells_list()  # Копируем все ячейки в отдельный список
        random.shuffle(cells)  # Перемешиваем
        # Для каждой ячейки в срезе длиной равной количеству бомб
        for cell in cells[:bombs]:
            cell.plant_bomb()  # Закладываем бомбу
            for adjacent_cell in self.get_adjacent_cells(cell.x, cell.y):  # Для соседних ячеек
                if not adjacent_cell.has_bomb():  # Если в них нет бомб
                    adjacent_cell.value += 1  # Увеличиваем значение
