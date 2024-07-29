"""Файл с классом для метода Дэвида-Флетчера-Пауэла"""
import sympy as sp
from other.operators import def_gradient
from methods.iteration_methods.quasi_newtonian_methods.quasi_newtonian import QuasiNewtonian

class DFPMethod(QuasiNewtonian):
    """Классом для метода Дэвида-Флетчера-Пауэла"""
    def calc_y(self):
        delta_x = sp.Matrix(self.dots[-1]) - sp.Matrix(self.dots[-2])
        return delta_x
    def calc_z(self):
        f = sp.Matrix(
            def_gradient(self.expr, self.current[0, 0], self.current[1, 0])
        )
        grad = sp.Matrix(
            def_gradient(self.expr, self.dots[-2][0], self.dots[-2][1])
        )
        g = f - grad
        return self.approx_inv_gesse * g
