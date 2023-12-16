"""Шаблон отчета итерационных методов"""

import matplotlib.pyplot as plt
from other.const import expr, folder
from other import my_io as io
from other.my_prettifier import tabulate_method_data, merge_table_with_headers
from other import graphics
from other.util import find_dots_bounds
from docx import Document
import other.docx_output as do
def report(header, method_obj, plot_name, file):
    """Формирует отчет"""
    io.output(f"\n-----{header}-----\n")
    io.output('Поиск первой длины шага с помощью одномерного поиска:')
    io.output(f'Начальный интервал неопределеннсти = {method_obj.t_interval}')
    io.output('Шаги вычисления:\n')
    for step in method_obj.t_steps:
        io.output(f"a = {round(step[0], 4)}, b = {round(step[1], 4)}")
    io.output("Таблица с шагами вычислений:")
    io.output(tabulate_method_data(method_obj.dots, method_obj.values))

    doc = Document()
    do.create_table_filled(
        document=doc,
        data=merge_table_with_headers(method_obj.dots, method_obj.values),
    )
    doc.save(f'{folder}/{file}.docx')

    plt.title(plot_name)
    graphics.level_lines(plt, expr, bounds=find_dots_bounds(method_obj.dots))
    graphics.dots_lines(plt, method_obj.dots)
    plt.savefig(f"{folder}/{file}.png")
    plt.clf()
