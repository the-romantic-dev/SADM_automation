from sympy import Rational, Matrix, symbols


def convert_to_rational_matrix(data: list[list[str]] | list[str]):
    rational_matrix = []

    def covert_to_rational_row(row: list[str]):
        rational_row = [Rational(coef) for coef in row]
        rational_matrix.append(rational_row)

    if isinstance(data[0], list):
        for r in data:
            covert_to_rational_row(r)
        return Matrix(rational_matrix)
    else:
        return Matrix(covert_to_rational_row(data))


class LPP:
    def __init__(self, A: list[list[str]], b: list[str], c: list[str]):
        self.A = convert_to_rational_matrix(A)
        self.b = convert_to_rational_matrix(b)
        self.c = convert_to_rational_matrix(c)

    @property
    def x(self):
        return symbols(f"x:{self.A.cols}")

    def is_canonical(self):
        return self.A.cols == 4

