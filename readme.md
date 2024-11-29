# Minesweeper

## Описание

Игра Сапёр на Python (2.7 / 3)

## Зависимости

- Python 2.7 или Python 3
- Библиотека Tkinter

## Запуск игры

```bash
python minesweeper.py
```

## Запуск тестов

```bash
python test.py
```


## Сборка

Установить зависимости, например pyinstaller

```bash
pip install -r requirements.txt
```

Запустить сборку

```bash
pyinstaller --onefile --windowed --icon icon.ico --add-data "icon.ico:." minesweeper.py
```