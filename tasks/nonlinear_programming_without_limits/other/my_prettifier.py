"""Наводит красоту и удобство в выводе"""
from sympy import Rational, pretty
from tabulate import tabulate
from .util import is_rational_finite_decimal
from .const import x1, x2


def rational_to_str(num: Rational):
    """Приводит к строке рациональное число"""
    result = str(num)
    q = num.q
    p = num.p

    if is_rational_finite_decimal(num):
        result = str(float(num))
    elif (abs(p) >= abs(q)):
        quotient, remainder = divmod(num, 1)
        result = f"{int(quotient)}+{remainder}"
    return result


def tabulate_method_data(dots, values):
    data = merge_table_with_headers(dots, values)
    return tabulate(data,
                    headers='firstrow',
                    tablefmt="grid",
                    colalign=("center", "center", "center", "center"))


def merge_table_with_headers(dots, values):
    headers = ["i", pretty(x1), pretty(x2), "f(X)"]
    data = []
    for i in range(len(dots)):
        item = [
            i,
            round(dots[i][0], 4),
            round(dots[i][1], 4),
            round(values[i], 4)]
        data.append(item)
    return [headers] + data
