from docx import Document
from sympy import symbols, Max, latex, Matrix

from methods.penalty_funcition_method import PenaltyFunctionMethod
from my_docx.docx_output import sympy2omml, create_table_filled, latex2omml


class PenaltyFunctionDocxFiller:
    def __init__(self, penalty_function):
        self.pf: PenaltyFunctionMethod = penalty_function

    def get_data_producers(self):
        return {
            'pf_equation': self._create_pf_equation,
            'pf_table': self._create_pf_table,
            'pf_pic': self._create_pf_pic,
            'pf_X': self._create_pf_X,
            'pf_f': self._create_pf_f
        }

    def _create_pf_equation(self):
        mu = symbols('μ')
        penalties = []
        for lim in self.pf.limits:
            penalties.append(Max(0, lim))

        penalty_sum = 0
        for elem in penalties:
            penalty_sum += elem
        return sympy2omml(mu * penalty_sum)

    def _create_pf_table(self):
        doc = Document()
        mu = symbols('μ')
        x1, x2 = symbols('x1 x2')
        table_len = len(self.pf.track)
        tabular_data = [
            ['i'] + [i for i in range(table_len)],
            [mu] + self.pf.all_mu,
            [x1] + [round(X[0, 0], 3) for X in self.pf.track],
            [x2] + [round(X[1, 0], 3) for X in self.pf.track],
            ['f'] + [round(value, 3) for value in self.pf.values_track],
        ]
        create_table_filled(doc, data=tabular_data)
        return doc

    def _create_pf_pic(self):
        return 'report_data/penalty_function.png'

    def _create_pf_X(self):
        return latex2omml('X^* = ' + latex(Matrix(
            [round(self.pf.solution['x1'], 3),
             round(self.pf.solution['x2'], 3)]
        )))

    def _create_pf_f(self):
        return latex2omml('f = ' + latex(round(self.pf.solution['f'], 3)))

