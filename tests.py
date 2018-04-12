# -*- coding: utf-8 -*-
from unittest import TestCase, main as run_tests
from entities import Field


def get_cells_coordinates(*cells):
    """Получает ячейки и возвращает список из кортежей с координатами этих ячеек
    :param cells: объекты класса Cell
    :return: list из tuple вида (cell.x, cell.y)
    """
    return [(cell.x, cell.y) for cell in cells]


def get_cells_coordinates_and_values(*cells):
    """Получает ячейки и возвращает список из кортежей с координатами и значениями этих ячеек
    :param cells: объекты класс Cell
    :return: list из tuple вида (cell.x, cell.y, cell.value)
    """
    return [(cell.x, cell.y, cell.value) for cell in cells]


class FieldTests(TestCase):
    """Тесткейсы игрового поля.
    Все тесты производятся над полем 3 на 3 вида
    | (0, 0) | (1, 0) | (2, 0) |
    | (0, 1) | (1, 1) | (2, 1) |
    | (0, 2) | (1, 2) | (2, 2) |
    """

    def test_get_cells(self):
        """Проверка метода получения ячейки"""
        x, y = 1, 1
        field = Field(width=3, height=3)
        cell = field.get_cell(x, y)
        self.assertEqual(x, cell.x)
        self.assertEqual(y, cell.y)

    def test_get_adjacent_cells_from_center_cell(self):
        """Проверка получения всех ячеек вокруг ячейки из центра.
        Сама ячейка не должна входить в последовательность"""
        expected_coordinates = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        x, y = 1, 1
        field = Field(width=3, height=3)
        cells_coordinates = get_cells_coordinates(*field.get_adjacent_cells(x, y))
        self.assertItemsEqual(expected_coordinates, cells_coordinates)

    def test_get_adjacent_cells_from_first_cell(self):
        """Проверка получения соседних ячеек для первой.
        Проверяется, что метод работает нормально для ячеек не имеющих соседей слева и сверху"""
        expected_coordinates = [(1, 0), (0, 1), (1, 1)]
        x, y = 0, 0
        field = Field(width=3, height=3)
        cells_coordinates = get_cells_coordinates(*field.get_adjacent_cells(x, y))
        self.assertItemsEqual(expected_coordinates, cells_coordinates)

    def test_get_adjacent_cells_from_last_cell(self):
        """Проверка получения соседних ячеек для последней.
        Проверяется, что метод работает нормально для ячеек не имеющих соседей справа и снизу"""
        expected_coordinates = [(1, 1), (2, 1), (1, 2)]
        x, y = 2, 2
        field = Field(width=3, height=3)
        cells_coordinates = get_cells_coordinates(*field.get_adjacent_cells(x, y))
        self.assertItemsEqual(expected_coordinates, cells_coordinates)

    def test_get_cell_with_bombs(self):
        """Проверка правильности получения ячеек с бомбами"""
        expected_coordinates = [(0, 1)]
        x, y = 0, 1
        field = Field(width=3, height=3)
        field.get_cell(x, y).plant_bomb()
        cells_coordinates = get_cells_coordinates(*field.get_cells_with_bombs())
        self.assertItemsEqual(expected_coordinates, cells_coordinates)

    def test_calculate_cells_values(self):
        """Проверка правильности вычисления значений ячеек, находящихся рядом с миной"""
        expected = [
            (0, 0, 1), (1, 0, -1), (2, 0, 1),
            (0, 1, 1), (1, 1, 1), (2, 1, 1),
            (0, 2, 0), (1, 2, 0), (2, 2, 0),
        ]
        expected_cells_with_bombs = [(1, 0)]
        field = Field(width=3, height=3)
        field.plant_random_bombs(bombs=1, seed=1000)
        cells_coordinates_and_values = get_cells_coordinates_and_values(*field.get_copy_cells_list())
        cells_with_bombs = get_cells_coordinates(*field.get_cells_with_bombs())
        self.assertItemsEqual(expected_cells_with_bombs, cells_with_bombs)
        self.assertItemsEqual(expected, cells_coordinates_and_values)

    def test_calculate_cells_values_for_two_bombs(self):
        """Проверка правильности вычисления значений ячеек, находящихся рядом с несколькими минами"""
        expected = [
            (0, 0, 1), (1, 0, -1), (2, 0, 1),
            (0, 1, 1), (1, 1, 2), (2, 1, 2),
            (0, 2, 0), (1, 2, 1), (2, 2, -1),
        ]
        expected_cells_with_bombs = [(1, 0), (2, 2)]
        field = Field(width=3, height=3)
        field.plant_random_bombs(bombs=2, seed=1000)
        cells_coordinates_and_values = get_cells_coordinates_and_values(*field.get_copy_cells_list())
        cells_with_bombs = get_cells_coordinates(*field.get_cells_with_bombs())
        self.assertItemsEqual(expected_cells_with_bombs, cells_with_bombs)
        self.assertItemsEqual(expected, cells_coordinates_and_values)

    def test_calculate_cells_values_for_many_bombs(self):
        """Проверка правильности вычисления значений ячеек, находящихся рядом с несколькими минами"""
        expected = [
            (0, 0, 3), (1, 0, -1), (2, 0, 2),
            (0, 1, -1), (1, 1, -1), (2, 1, 4),
            (0, 2, 3), (1, 2, -1), (2, 2, -1),
        ]
        expected_cells_with_bombs = [(1, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
        field = Field(width=3, height=3)
        field.plant_random_bombs(bombs=5, seed=1000)
        cells_coordinates_and_values = get_cells_coordinates_and_values(*field.get_copy_cells_list())
        cells_with_bombs = get_cells_coordinates(*field.get_cells_with_bombs())
        self.assertItemsEqual(expected_cells_with_bombs, cells_with_bombs)
        self.assertItemsEqual(expected, cells_coordinates_and_values)


if __name__ == '__main__':
    run_tests()
