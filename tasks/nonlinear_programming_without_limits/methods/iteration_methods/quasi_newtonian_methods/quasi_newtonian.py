"""Файл с родительским классом для квази-ньютоновских методов"""
import sympy as sp
from methods.iteration_methods.iteration import IterationMethod
from other.operators import def_gradient


class QuasiNewtonian(IterationMethod):
    """Родительский класс для квази-ньютоновских методов"""

    approx_inv_gesse = None

    def calc_k(self):
        self.calc_approx_inv_gesse()
        return (
            -1
            * self.approx_inv_gesse
            * sp.Matrix(def_gradient(self.expr, self.current[0, 0], self.current[1, 0]))
        )

    def calc_approx_inv_gesse(self):
        """Вычисляет аппроксимированное значение обратной матрцы Гессе и
        записывает его в approx_inv_gesse"""
        if self.approx_inv_gesse is None or self.steps_num == 0:
            self.approx_inv_gesse = -sp.Matrix.eye(2, 2)
        else:
            delta_x = sp.Matrix(self.dots[-1]) - sp.Matrix(self.dots[-2])
            y = self.calc_y()
            z = self.calc_z()
            f = sp.Matrix(
                def_gradient(self.expr, self.current[0, 0], self.current[1, 0])
            )
            grad = sp.Matrix(
                def_gradient(self.expr, self.dots[-2][0], self.dots[-2][1])
            )
            g = f - grad
            a = (delta_x * y.T) / (y.T * g).det()
            b = (self.approx_inv_gesse * g * z.T) / (z.T * g).det()
            increment = a - b
            self.approx_inv_gesse = self.approx_inv_gesse + increment

    def calc_y(self):
        """Вычисление вектора Y"""
        return sp.Matrix(1, 1)

    def calc_z(self):
        """Вычисление вектора Z"""
        return sp.Matrix(1, 1)
