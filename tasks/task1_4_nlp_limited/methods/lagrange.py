import sympy as sp
from sympy import Matrix

import plotter
import util

class Lagrange:
    def __init__(self) -> None:
        self.f = None
        self.lim = None
        self._lagrange = None
        self._eq1 = None
        self._eq2 = None
        self._eq3 = None
        self._linsolve = None
        self.opt_dot = None
        self.opt_value = None
        self._gesse = None
        self._det = None
    
    def solve(self, f, limitation):
        self.f = f
        self.lim = limitation
        v, x1, x2 = sp.symbols('v x1 x2')
        self._lagrange = f + v * limitation
        self._eq1 = sp.diff(self._lagrange, x1)
        self._eq2 = sp.diff(self._lagrange, x2)
        self._eq3 = sp.diff(self._lagrange, v)
        A, b = sp.linear_eq_to_matrix([self._eq1, self._eq2, self._eq3], [v, x1, x2])
        self._linsolve = sp.linsolve((A, b), [v, x1, x2]).args[0]
        self.opt_dot = [self._linsolve[1], self._linsolve[2]]
        self.opt_value = f.subs({x1: self.opt_dot[0], x2: self.opt_dot[1]})
        self._gesse = util.gesse()
        x_res = sp.Matrix(self.opt_dot)
        self._det = (x_res.T * self._gesse * x_res).det()

    def prepare_plot(self):
        plotter.plt.figure(figsize=(15, 9))
        plotter.clear()
        # limits_intersects = plotter.get_limits_points(self.limits)
        bounds = {"min": [-10, -10], "max": [10, 10]}
        plotter.add_level_lines(self.f, bounds)
        plotter.add_linear_eq_limitation(self.lim, bounds)
        plotter.plt.scatter(
            self.opt_dot[0],
            self.opt_dot[1],
            marker='o',
            color='red')

    def show_plot(self):
        self.prepare_plot()
        plotter.show()

    def save_plot(self, path: str):
        self.prepare_plot()
        plotter.save(path)


    def report(self, output_func):
        output_func("|---------------------------------------------------------|")
        output_func("|----------------ОТЧЕТ ПО МЕТОДУ ЛАГРАНЖА-----------------|")
        output_func("|---------------------------------------------------------|")
        output_func(f"Функция Лагранжа:\n{sp.pretty(self._lagrange)}\n")
        output_func(f"Eq1: {sp.pretty(self._eq1)}")
        output_func(f"Eq2: {sp.pretty(self._eq2)}")
        output_func(f"Eq3: {sp.pretty(self._eq3)}\n")
        output_func(f'Решение системы уравнений:\n{sp.pretty(sp.Matrix(self._linsolve).T)}\n')
        output_func(f'Матрица Гессе:\n{sp.pretty(self._gesse)}\n')
        output_func(f'Определенность: {self._det} = {round(float(self._det), 3)}\n')
        output_func(f'X_opt: {self.opt_dot} = {[round(float(n), 3) for n in self.opt_dot]}\n')
        output_func(f'F_opt: {self.opt_value} = {round(float(self.opt_value), 3)}\n')