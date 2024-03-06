"""Контроллер ввода/вывода данных"""
from other.const import folder

output_file = f"{folder}/output.txt"

def output(data=""):
    """Вывод данных"""
    add_to_file(data)

def add_to_file(string):
    """Добавляет вывод в файл"""
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(string + "\n")

def clear_output():
    """Очищает файл вывода"""
    open(output_file, 'w', encoding="utf-8").close()
