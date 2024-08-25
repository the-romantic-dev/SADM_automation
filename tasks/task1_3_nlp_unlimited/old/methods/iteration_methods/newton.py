"""Работает с методом Ньютона безусловной оптимизации ЗНЛП"""
import sympy as sp
from methods.iteration_methods.iteration import IterationMethod
from other.operators import def_gradient, gesse

class NewtonMethod(IterationMethod):
    """Класс для работы с методом Ньютона безусловной оптимизации ЗНЛП"""

    def calc_k(self):
        grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
        inversed_def_gesse = sp.Matrix(gesse(self.expr)).inv()

        return -inversed_def_gesse * sp.Matrix(grad)

    def calc_t(self):
        return 1
