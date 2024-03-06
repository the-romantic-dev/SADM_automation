"""Файл с классом метода штрафных функция"""
import sympy as sp
from sympy import Rational
from tabulate import tabulate

import util
from .npp_method import NPPMethod

x1, x2 = sp.symbols('x1 x2')


def psi(y):
    """Функия psi для построения барьерной функции"""
    return -sp.ln(-y)
    # return -1 / y ** 3


def build_barrier(limitations):
    """Строит барьер для барьерной функции"""
    result = 0
    for g in limitations:
        result += psi(g)
    return result


def is_solution_possible(solution, limits):
    result = True
    tol = 1e-3
    for lim in limits:
        if lim.subs({x1: solution[0, 0], x2: solution[1, 0]}) > tol:
            result = False
            break
    return result


class BarrierFunctionMethod(NPPMethod):
    """Класс метода барьерных функций"""
    tol = 1e-4

    def __init__(self):
        super().__init__()
        self.all_mu = []

    def solve(self, f, limitations, start):
        """Решает ЗНП методом барьерных функций.
        Метод является методом внутренней точки, поэтому точка start должна лежать В
        области допустимых значений limitations
        """
        X = start
        self.track.append(X)
        self.f = f
        self.limits = limitations
        self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
        delta_x = 1
        delta_f = 1
        mu = 100
        mu_factor = 10
        barrier = build_barrier(limitations)

        while delta_x > self.tol and delta_f > self.tol:
            barrier_f = f - mu * barrier
            new_X = util.optimize(barrier_f, X)
            # if not is_solution_possible(new_X, limitations):
            #     break
            delta_x = (X - new_X).norm()
            delta_f = abs(f.subs({x1: X[0, 0], x2: X[1, 0]}) - f.subs({x1: new_X[0, 0], x2: new_X[1, 0]}))
            X = new_X
            self.track.append(X)
            self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
            self.all_mu.append(mu)
            mu /= mu_factor
        self.solution['x1'] = X[0, 0]
        self.solution['x2'] = X[1, 0]
        self.solution['f'] = f.subs({x1: X[0, 0], x2: X[1, 0]})

    def get_report(self):
        """Формирует строку с отчетом по работе метода"""
        header = """
        |---------------------------------------------------------|
        |------------ОТЧЕТ ПО МЕТОДУ БАРЬЕРНЫХ ФУНКЦИЙ------------|
        |---------------------------------------------------------|
        """
        mu = sp.symbols('μ')
        penalty_strs = []
        for lim in self.limits:
            penalty_strs.append(f"ln({-lim})")

        penalty_function = f'f + {sp.pretty(mu)}⋅({" + ".join(penalty_strs)})'
        table_len = len(self.track)
        tabular_data = [
            ['i'] + [i for i in range(table_len)],
            [sp.pretty(mu)] + self.all_mu,
            [sp.pretty(x1)] + [float(X[0, 0]) for X in self.track],
            [sp.pretty(x2)] + [float(X[1, 0]) for X in self.track],
            ['f'] + [value for value in self.values_track],
        ]
        tolerance = f"Погрешность: {self.tol}"
        table = tabulate(
            tabular_data,
            headers='firstrow',
            tablefmt="grid",
            floatfmt=('.3f' for i in range(table_len)),
            colalign=('center' for i in range(table_len))
        )

        result = '\n\n'.join([
            header,
            "Барьер:",
            penalty_function,
            tolerance,
            "Таблица шагов:",
            table
        ])
        return result

    def create_doc(self, name: str):
        from sympy import pretty
        from my_docx import docx_output
        from my_io import io
        from docx import Document

        doc = Document()
        table_len = len(self.track)
        data = [
            ['i'] + [i for i in range(table_len)],
            ['μ'] + [m for m in self.all_mu],
            [pretty(x1)] + [round(float(X[0, 0]), 3) for X in self.track],
            [pretty(x2)] + [round(float(X[1, 0]), 3) for X in self.track],
            ['f'] + [round(value, 3) for value in self.values_track],
        ]
        docx_output.create_table_filled(
            document=doc,
            data=data
        )
        io.save_doc(doc=doc, name=name)
