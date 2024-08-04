from dataclasses import dataclass

from sympy import Rational, Matrix


@dataclass
class LPPData:
    c: list[Rational]
    a: list[list[Rational]]
    b: list[Rational]


def get_canonical_form(lpp_data: LPPData) -> LPPData:
    """Возвращает коэффициенты канонической формы. Применимо для любого количества переменных"""
    a = lpp_data.a
    b = lpp_data.b
    c = lpp_data.c

    result_c = c + [Rational(0) for _ in range(len(c))]
    result_a = []
    result_b = []

    for i, be in enumerate(b):
        # Дополнение коэффициентов искусственных переменных
        additional_a = [Rational(0) for _, _ in enumerate(a)]
        if be >= 0:
            row_factor = Rational(1)
        else:
            row_factor = Rational(-1)

        result_b.append(b[i] * row_factor)
        additional_a[i] = row_factor
        result_a.append([a_ij * row_factor for _, a_ij in enumerate(a[i])] + additional_a)

    return LPPData(c=result_c, a=result_a, b=result_b)


def get_column(col: int, matrix: list[list]):
    n = len(matrix)
    result = []
    for i in range(n):
        result.append(matrix[i][col])
    return result
