"""Файл с классом метода штрафных функция"""
import sympy as sp
import util
from tabulate import tabulate
from .npp_method import NPPMethod
from docx import Document

x1, x2 = sp.symbols('x1 x2')


def psi(y):
    """Функия psi для построения штрафной функции"""
    return sp.Piecewise((0, y < 0), (y, y >= 0))


def build_penalty(limitations):
    """Строит штраф для штрафной функции"""
    result = 0
    for lim in limitations:
        result += psi(lim)
    return result


class PenaltyFunctionMethod(NPPMethod):
    """Класс метода штрафных функций"""
    tol = 1e-3

    def __init__(self):
        super().__init__()
        self.all_mu = []
        self.penalty = None

    def solve(self, f, limitations, start):
        """Решает ЗНП методом штрафных функций.
        Метод является методом внешней точки, поэтому точка start должна лежать ВНЕ
        области допустимых значений limitations
        """
        X = start
        self.track.append(X)
        self.f = f
        self.limits = limitations
        self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
        delta_x = 1
        mu = 0.001
        mu_factor = 10
        penalty = build_penalty(limitations)
        while delta_x > self.tol:
            penalty_f = f - mu * penalty
            new_X = util.optimize(penalty_f, X)
            delta_x = (X - new_X).norm()
            X = new_X
            self.track.append(X)
            self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
            self.all_mu.append(mu)
            mu *= mu_factor
        self.solution['x1'] = X[0, 0]
        self.solution['x2'] = X[1, 0]
        self.solution['f'] = f.subs({x1: X[0, 0], x2: X[1, 0]})

    def get_report(self):
        """Формирует строку с отчетом по работе метода"""
        header = """
        |---------------------------------------------------------|
        |------------ОТЧЕТ ПО МЕТОДУ ШТРАФНЫХ ФУНКЦИЙ-------------|
        |---------------------------------------------------------|
        """
        mu = sp.symbols('μ')
        penalty_strs = []
        for lim in self.limits:
            penalty_strs.append(f"max(0, {lim})")

        penalty_function = f'f - {sp.pretty(mu)}⋅({" + ".join(penalty_strs)})'
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
            "Штраф:",
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
        doc = Document()
        table_len = len(self.track)
        data = [
            ['i'] + [i for i in range(table_len)],
            ['μ'] + [mu for mu in self.all_mu],
            [pretty(x1)] + [round(float(X[0, 0]), 3) for X in self.track],
            [pretty(x2)] + [round(float(X[1, 0]), 3) for X in self.track],
            ['f'] + [round(value, 3) for value in self.values_track],
        ]
        docx_output.create_table_filled(
            document=doc,
            data=data
        )
        io.save_doc(doc=doc, name=name)
