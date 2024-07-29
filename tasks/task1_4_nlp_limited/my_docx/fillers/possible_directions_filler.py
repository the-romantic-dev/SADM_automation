from docx import Document
from sympy import symbols, latex, Matrix

from methods.possible_directions import PossibleDirections
from my_docx.docx_output import sympy2omml, create_table_filled, latex2omml


def try_round(arg, accuracy):
    try:
        return round(arg, accuracy)
    except:
        return arg


class PossibleDirectionsDocxFiller:
    def __init__(self, possible_directions):
        self.pd: PossibleDirections = possible_directions

    def get_data_producers(self):
        return {
            'pd_start_solution': self._create_pd_start_solution,
            'pd_table': self._create_pd_table,
            'pd_pic': self._create_pd_pic,
            'pd_X': self._create_pd_X,
            'pd_f': self._create_pd_f
        }

    def _create_pd_start_solution(self):
        return sympy2omml(self.pd.track[0])

    def _create_pd_table(self):
        doc = Document()
        x1, x2 = symbols('x1 x2')
        table_len = len(self.pd.track)
        tabular_data = [
            ['i'] + [i for i in range(table_len)],
            [x1] + [round(X[0, 0], 3) for X in self.pd.track],
            [x2] + [round(X[1, 0], 3) for X in self.pd.track],
            ['u'] + [try_round(u, 3) for u in self.pd.u_track],
            ['f'] + [round(value, 3) for value in self.pd.values_track],
        ]
        create_table_filled(doc, data=tabular_data)
        return doc

    def _create_pd_pic(self):
        return 'report_data/possible_directions.png'

    def _create_pd_X(self):
        return latex2omml('X^* = ' + latex(Matrix(
            [round(self.pd.solution['x1'], 3),
             round(self.pd.solution['x2'], 3)]
        )))

    def _create_pd_f(self):
        return latex2omml('f = ' + latex(round(self.pd.solution['f'], 3)))