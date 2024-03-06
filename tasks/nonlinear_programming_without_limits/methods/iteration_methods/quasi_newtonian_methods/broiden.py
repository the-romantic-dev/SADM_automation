"""Файл с классом для метода Бройдена"""
import sympy as sp

from tasks.nonlinear_programming_without_limits.methods.iteration_methods.quasi_newtonian_methods.quasi_newtonian import QuasiNewtonian
from tasks.nonlinear_programming_without_limits.other.operators import def_gradient


class BroidenMethod(QuasiNewtonian):
    """Классом для метода Бройдена"""
    def calc_y(self):
        delta_x = sp.Matrix(self.dots[-1]) - sp.Matrix(self.dots[-2])
        f = sp.Matrix(
            def_gradient(self.expr, self.current[0, 0], self.current[1, 0])
        )
        grad = sp.Matrix(
            def_gradient(self.expr, self.dots[-2][0], self.dots[-2][1])
        )
        g = f - grad
        return delta_x - self.approx_inv_gesse * g

    def calc_z(self):
        return self.calc_y()
