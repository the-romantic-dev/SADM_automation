"""Файл с родительским классом для итерационных методов"""
import sympy as sp
import util
tol = 1e-1
x1,x2 = sp.symbols('x1 x2')

class IterationMethod:
    """Родительский класс для итерационных методов"""
    # dots = []
    # values = []
    # expr = None
    # steps_num = 0
    # current = None

    def __init__(self, start, expr):
        self.dots = []
        self.values = []
        self.expr = expr
        self.steps_num = 0
        self.current = sp.Matrix(start)
        self.dots.append(start)
        self.values.append(self.expr.subs({x1: start[0], x2: start[1]}))
        self.start_method()

    def start_method(self):
        """Запускает ход метода"""
        k = self.calc_k()
        t = self.calc_t()

        grad = util.gradient(self.current)
        while grad.norm() > tol:
            self.steps_num += 1
            x_i = self.current + t * k
            self.dots.append(x_i.T.tolist()[0])
            self.values.append(self.expr.subs({x1: x_i[0,0], x2: x_i[1,0]}))
            self.current = x_i
            grad = util.gradient(self.current)
            k = self.calc_k()
            t = self.calc_t()

    def calc_k(self):
        """Вычисление направления шага (k)"""
        return sp.Matrix(1,1)

    def calc_t(self):
        """Вычисление длины шага (t)"""
        grad = util.gradient(self.current)
        gesse_matrix = sp.Matrix(util.gesse(self.current))
        k = self.calc_k()
        a = grad.T * k
        b = k.T * gesse_matrix * k
        t_i = -a.det() / b.det()
        return t_i

    # def gradient(self, X = None):
    #     x1, x2 = sp.symbols('x1 x2')
    #     result = sp.Matrix([[sp.diff(self.expr, x1)],
    #                         [sp.diff(self.expr, x2)]])
    #     if not X is None:
    #         result = result.subs({x1: X[0,0], x2: X[1,0]})
    #     return result

    # def gesse(self, X = None):
    #     result = sp.Matrix([[sp.diff(self.expr, x1, x1), sp.diff(self.expr, x1, x2)],
    #                         [sp.diff(self.expr, x2, x1), sp.diff(self.expr, x2, x2)]])
    #     if not X is None:
    #         result = result.subs({x1: X[0,0], x2: X[1,0]})
    #     return result
