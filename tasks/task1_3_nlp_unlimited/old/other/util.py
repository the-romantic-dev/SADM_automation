"""Вспомогательные функции"""
from sympy import Rational

def find_dots_bounds(dots):
    """Поиск крайних точек в массиве"""
    min_x1 = None
    min_x2 = None
    max_x1 = None
    max_x2 = None

    for d in dots:
        if (min_x1 is None or min_x1 > d[0]):
            min_x1 = d[0]
        if (min_x2 is None or min_x2 > d[1]):
            min_x2 = d[1]
        if (max_x1 is None or max_x1 < d[0]):
            max_x1 = d[0]
        if (max_x2 is None or max_x2 < d[1]):
            max_x2 = d[1]

    return {"min": [min_x1, min_x2], "max": [max_x1, max_x2]}

def is_rational_finite_decimal(num: Rational):
    """Проверяем, является ли рациональная дробь конечной десятичной дробью"""
    # Проверяем, является ли знаменатель степенью 2 или 5
    q = num.q
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5

    # Если знаменатель равен 1, то дробь конечная
    return q == 1
