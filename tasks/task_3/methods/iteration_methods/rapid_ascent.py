"""Работает с методом наискорейшего подъема безусловной оптимизации ЗНЛП"""
import sympy as sp
from methods.iteration_methods.iteration import IterationMethod
from other.operators import def_gradient

class RapidAscentMethod(IterationMethod):
    """Класс для работы с методом наискорейшего подъема безусловной оптимизации ЗНЛП"""
    def calc_k(self):
        return sp.Matrix(def_gradient(self.expr, self.current[0,0], self.current[1,0]))

    # def calc_t(self):
    #     grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
    #     grad = sp.Matrix(grad)
    #     gesse_matrix = sp.Matrix(gesse(self.expr))
    #     k = self.calc_k()
    #     a = grad.T * k
    #     b = k.T * gesse_matrix * k
    #     t_i = -a.det() / b.det()
    #     return t_i
