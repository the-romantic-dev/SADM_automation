"""Класс, содержащий начальную задачу"""
from tasks.task1_4_nlp_limited.old.my_io.io import A, B, C, D
import sympy as sp


class Task:
    """Класс, содержащий начальную задачу"""
    x1, x2 = sp.symbols('x1 x2')

    f = C['C11'] * x1 ** 2 + C['C22'] * x2 ** 2 + C['C12'] * x1 * x2 + C['C1'] * x1 + C['C2'] * x2

    lim1234 = []
    try:
        lim1234 = [
            A['A11'] * x1 + A['A12'] * x2 - B['B1'],
            A['A21'] * x1 + A['A22'] * x2 - B['B2'],
            A['A31'] * x1 + A['A32'] * x2 - B['B3'],
            A['A41'] * x1 + A['A42'] * x2 - B['B4']
        ]
    except KeyError:
        lim1234 = [
            A['A11'] * x1 + A['A12'] * x2 - B['B1'],
            A['A21'] * x1 + A['A22'] * x2 - B['B2'],
            -x1,
            -x2
        ]

    lim5 = A['A51'] * x1 + A['A52'] * x2 - B['B5']

    lim67 = []
    try:
        lim67 = [
            D['D11'] * x1 ** 2 + D['D22'] * x2 ** 2 - B['B6'],
            D['D33'] * x1 ** 2 + D['D44'] * x2 ** 2 - B['B7']
        ]
    except:
        lim67 = [
            D['D11'] * x1 ** 2 + D['D22'] * x2 ** 2 - B['B6']
        ]

