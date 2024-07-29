import dataclasses

from sympy import Rational

omegas = [
    Rational(9, 38),
    Rational(9, 38),
    Rational(9, 38),
    Rational(10, 38),
    Rational(1, 38)
]

intensities = [
    (Rational(7), Rational(8)),
    (Rational(10), Rational(10)),
    (Rational(1, 2), Rational(1)),
    (Rational(5), Rational(10)),
    (Rational(1, 4), Rational(1, 2))
]

channels = [1, 1, 18, 18, 18]
def mu(i, k):
    return min(k, channels[i]) * mus[i]


def z(n: tuple[int]):
    total = sum(n)

