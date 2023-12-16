"""Работает с аналитическим методом безусловной оптимизации ЗНЛП"""
import sympy as sp
from other.const import x1,x2
from other.operators import gradient, gesse

class Analytic:
    """Класс для работы с аналитическим методом безусловной оптимизации ЗНЛП"""
    expr = None
    gesse = None
    solution = None
    grad = None
    quadratic_form = None

    def __init__(self, expr):
        self.expr = expr
        self.grad = gradient(expr)
        self.gesse = gesse(expr)

        solution = self.calc_solution(gradient(expr))
        self.solution = solution

        quadratic_form = self.calc_quadratic_form(expr, solution)
        self.quadratic_form = quadratic_form

    def calc_solution(self, grad):
        """Считает решение при grad = 0"""
        equations = (sp.Eq(grad[0], 0), sp.Eq(grad[1], 0))
        return sp.solve(equations, (x1, x2))

    def calc_quadratic_form(self,expr, solution):
        """Считает квадратичную форму матрицы Гессе с решением при grad=0"""
        matrix_gesse = sp.Matrix(gesse(expr))
        matrix_solution = sp.Matrix([solution[x1], solution[x2]])
        return sp.det(matrix_solution.T * matrix_gesse * matrix_solution)
