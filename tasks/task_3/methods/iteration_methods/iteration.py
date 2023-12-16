"""Файл с родительским классом для итерационных методов"""
import sympy as sp
from other.const import x1,x2,tol
from other.operators import def_gradient, gesse

def univariate_step(X, K, f) -> float:
    golden_tol = 1e-3
    golden = 1.618
    t = sp.symbols("t")
    solution = X + t * K
    value = f.subs({x1: solution[0,0], x2: solution[1,0]})
    steps = []
    
    def undefined_interval():
        t0 = 0
        t1 = 1
        f0 = value.subs({t: t0})
        f1 = value.subs({t: t1})
        while True:
            t2 = t1 + 1.62 * (t1 - t0)
            f2 = value.subs({t: t2})
            if f2 < f1:
                break
            f0 = f1
            f1 = f2
            t0 = t1
            t1 = t2
        return [t0, t2]
        
    def step(a,b):
        x_1 = b - (b-a)/golden
        x_2 = a + (b-a)/golden
        y_1 = value.subs({t: x_1})
        y_2 = value.subs({t: x_2})
        if y_1 <= y_2:
            a = x_1
        else:
            b= x_2
        return a,b
    interval = undefined_interval()
    a,b = interval
    steps.append((a,b))
    while abs(a - b) >= golden_tol:
        a,b = step(a,b)
        steps.append((a,b))
    return (a+b)/2, interval, steps

class IterationMethod:
    """Родительский класс для итерационных методов"""

    def __init__(self, start, expr):
        self.dots = []
        self.values = []
        self.expr = expr
        self.t_interval = None
        self.t_steps = None
        self.steps_num = 0
        self.current = sp.Matrix(start)
        self.dots.append(start)
        self.values.append(self.expr.subs({x1: start[0], x2: start[1]}))
        self.start_method()

    def start_method(self):
        """Запускает ход метода"""
        k = self.calc_k()
        t, self.t_interval, self.t_steps = univariate_step(self.current, k, self.expr)
        # t = self.calc_t()
        grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
        while sp.Matrix(grad).norm() > tol:
            self.steps_num += 1
            x_i = self.current + t * k
            self.dots.append(x_i.T.tolist()[0])
            self.values.append(self.expr.subs({x1: x_i[0,0], x2: x_i[1,0]}))
            self.current = x_i
            grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
            k = self.calc_k()
            t = self.calc_t()

    def calc_k(self):
        """Вычисление направления шага (k)"""
        return sp.Matrix(1,1)

    def calc_t(self):
        """Вычисление длины шага (t)"""
        t = None
        grad = def_gradient(self.expr, self.current[0,0], self.current[1,0])
        grad = sp.Matrix(grad)
        gesse_matrix = sp.Matrix(gesse(self.expr))
        k = self.calc_k()
        a = grad.T * k
        b = k.T * gesse_matrix * k
        t = -a.det() / b.det()
        return t
