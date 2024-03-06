from docx import Document
from sympy import symbols, ln, latex, Matrix

from methods.barrier_funcition_method import BarrierFunctionMethod
from my_docx.docx_output import sympy2omml, create_table_filled, latex2omml


class BarrierFunctionDocxFiller:

    def __init__(self, barrier_function):
        self.bf: BarrierFunctionMethod = barrier_function

    def get_data_producers(self):
        return {
            'bf_equation': self._create_bf_equation,
            'bf_table': self._create_bf_table,
            'bf_pic': self._create_bf_pic,
            'bf_X': self._create_bf_X,
            'bf_f': self._create_bf_f
        }

    def _create_bf_equation(self):
        mu = symbols('μ')
        penalties = []
        for lim in self.bf.limits:
            penalties.append(f'\ln({latex(-lim)})')

        penalty_sum = " + ".join(penalties)
        return latex2omml(f'μ ({penalty_sum})')

    def _create_bf_table(self):
        doc = Document()
        mu = symbols('μ')
        x1, x2 = symbols('x1 x2')
        table_len = len(self.bf.track)
        tabular_data = [
            ['i'] + [i for i in range(table_len)],
            [mu] + [round(i, 10) for i in self.bf.all_mu],
            [x1] + [round(X[0, 0], 3) for X in self.bf.track],
            [x2] + [round(X[1, 0], 3) for X in self.bf.track],
            ['f'] + [round(value, 3) for value in self.bf.values_track],
        ]
        create_table_filled(doc, data=tabular_data)
        return doc

    def _create_bf_pic(self):
        return 'report_data/barrier_function.png'

    def _create_bf_X(self):
        return latex2omml('X^* = ' + latex(Matrix(
            [round(self.bf.solution['x1'], 3),
             round(self.bf.solution['x2'], 3)]
        )))

    def _create_bf_f(self):
        return latex2omml('f = ' + latex(round(self.bf.solution['f'], 3)))
