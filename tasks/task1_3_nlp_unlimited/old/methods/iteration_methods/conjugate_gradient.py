"""Работает с методом Ньютона безусловной оптимизации ЗНЛП"""
import sympy as sp
from methods.iteration_methods.iteration import IterationMethod
from other.operators import def_gradient


class ConjugateGradientMethod(IterationMethod):
    """Класс для работы с методом Ньютона безусловной оптимизации ЗНЛП"""

    def calc_k(self):
        grad = sp.Matrix(def_gradient(self.expr, self.current[0, 0], self.current[1, 0]))
        if self.steps_num == 0:
            return grad
        else:
            last_dot = self.dots[-2]
            last_grad = sp.Matrix(def_gradient(self.expr, last_dot[0], last_dot[1]))
            return grad + (grad.norm() ** 2 / last_grad.norm() ** 2) * last_grad

    # def calc_t(self):
    #     grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
    #     grad = sp.Matrix(grad)
    #     gesse_matrix = sp.Matrix(gesse(self.expr))
    #     k = self.calc_k()
    #     a = grad.T * k
    #     b = k.T * gesse_matrix * k
    #     t_i = -a.det() / b.det()
    #     return t_i
