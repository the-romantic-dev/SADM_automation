from functools import cached_property

from sympy import Rational, symbols, diff, Matrix


class NLPObjective:
    def __init__(self, coeffs: list[Rational]):
        self.coeffs = coeffs

    @cached_property
    def variables(self):
        return list(symbols('x1 x2'))

    @cached_property
    def expr(self):
        x1, x2 = self.variables
        C = self.coeffs
        return C[0] * x1 ** 2 + C[1] * x2 ** 2 + C[2] * x1 * x2 + C[3] * x1 + C[4] * x2

    def grad(self, point: list[Rational] = None):
        result = [diff(self.expr, x) for x in self.variables]
        if point is not None:
            x1, x2 = self.variables
            if len(point) != len(self.variables):
                raise ValueError("Incorrect point")
            result = [item.subs({x1: point[0], x2: point[1]}) for item in result]
        return result

    def gesse(self):
        grad = self.grad()
        result = [
            [diff(item, x) for x in self.variables] for item in grad
        ]
        return result

    def value(self, point_vector: Matrix):
        solution = point_vector.T.tolist()[0]
        subs = {x: sol for x, sol in zip(self.variables, solution)}
        return self.expr.subs(subs)
