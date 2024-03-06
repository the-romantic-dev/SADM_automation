from sympy import Rational
"""Модуль для работы с вводом/выводом"""
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

def folder_path():
    """Считывает из файла путь до папки с отчетом"""
    with open("folder.txt", "r", encoding="utf-8") as file:
        for line in file:
            return line

def read_input(filename: str) -> dict:
    """Считывает файлы с входными данными"""
    result = {}
    with open(f'{folder}/{filename}', 'r', encoding="utf-8") as file:
        for line in file:
            key, value = map(str.strip, line.split(':'))
            value = Rational(value)
            result[key] = value
    return result

def save_doc(doc, name:str):
    doc.save(f"{folder}/{name}")

folder = folder_path()
output_file = f"{folder}/output.txt"
A = read_input(filename = "A.txt")
B = read_input(filename = "B.txt")
C = read_input(filename = "C.txt")
D = read_input(filename = "D.txt")



