"""Формирует отчет аналитического метода"""
from sympy import pretty, Matrix

from methods.analytic import Analytic
from other.const import expr, x1, x2
from other.my_prettifier import rational_to_str
import other.my_io as io

analytic = Analytic(expr)

def report():
    """Формирует отчет аналитического метода"""
    io.output("\n-----АНАЛИТИЧЕСКИЙ МЕТОД-----\n")
    io.output(f"Градиент:\n{pretty(Matrix(analytic.grad))}\n")
    sol = Matrix([
        rational_to_str(analytic.solution[x1]),
        rational_to_str(analytic.solution[x2])])
    io.output(f"Оптимальное решение:\n{pretty(sol)}\n")
    io.output(f"Матрица Гессе:\n{pretty(Matrix(analytic.gesse))}\n")
    io.output(f"Определенность матрицы Гессе:\n{analytic.quadratic_form}\n")
    io.output(f"Оптимальное значение функции:\n{expr.subs(analytic.solution)}")
