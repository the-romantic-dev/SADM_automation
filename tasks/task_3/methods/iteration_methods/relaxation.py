"""Работает с релаксационным методом безусловной оптимизации ЗНЛП"""
import sympy as sp
from methods.iteration_methods.iteration import IterationMethod
from other.operators import def_gradient

class RelaxationMethod(IterationMethod):
    """Класс для работы с релаксационным методом безусловной оптимизации ЗНЛП"""
    
    def calc_k(self):
        grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
        if self.steps_num % 2 == 0:
            return sp.Matrix([grad[0], 0])
        else:
            return sp.Matrix([0, grad[1]])

    # def calc_t(self):
    #     grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
    #     grad = sp.Matrix(grad)
    #     gesse_matrix = sp.Matrix(gesse(self.expr))
    #     k = self.calc_k()
    #     a = grad.T * k
    #     b = k.T * gesse_matrix * k
    #     t_i = -a.det() / b.det()
    #     return t_i
