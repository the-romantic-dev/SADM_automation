from sympy import latex, Eq, symbols, Matrix
from my_docx.docx_output import latex2omml, sympy2omml
from task import Task

dL, dx1, dx2, dv1, v1 = symbols('∂L ∂x_1 ∂x_2 ∂v_1 v_1')


class LagrangeDocxFiller:

    def __init__(self, lagrange):
        self._lagrange = lagrange

    def _create_lagrange_eq1(self):
        return latex2omml(latex(Eq(dL / dx1, self._lagrange._eq1)) + ' = 0')

    def _create_lagrange_eq2(self):
        return latex2omml(latex(Eq(dL / dx2, self._lagrange._eq2)) + ' = 0')

    def _create_lagrange_eq3(self):
        return latex2omml(latex(Eq(dL / dv1, self._lagrange._eq3)) + ' = 0')

    def _create_lagrange_gesse(self):
        formula = r'H_L (X,V)=\left\{ \frac{∂^2 L(X,V)}{(∂x_i ∂x_j )} \right\}_{i,j=\overline{1,n}}='
        return latex2omml(formula + latex(self._lagrange._gesse))

    def _create_lagrange_u(self):
        return sympy2omml(Eq(v1, self._lagrange._linsolve[2]))

    def _create_lagrange_X(self):
        return latex2omml('X^* = ' + latex(Matrix(self._lagrange.opt_dot)))

    def _create_lagrange_det(self):
        return latex2omml('{X^{*}}^T⋅H_L (X^*,V)⋅X^* = ' + latex(self._lagrange._det))

    def _create_lagrange_f(self):
        return latex2omml('f = ' + latex(self._lagrange.opt_value))

    def get_data_producers(self):
        return {
            'lagrange_eq1': self._create_lagrange_eq1,
            'lagrange_eq2': self._create_lagrange_eq2,
            'lagrange_eq3': self._create_lagrange_eq3,
            'lagrange_gesse': self._create_lagrange_gesse,
            'lagrange_u': self._create_lagrange_gesse,
            'lagrange_X': self._create_lagrange_X,
            'lagrange_det': self._create_lagrange_det,
            'lagrange_f': self._create_lagrange_f,
            'lim5_expr': lambda: sympy2omml(Task.lim5)

        }
