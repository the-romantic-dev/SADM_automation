from numpy import sign
from sympy import Rational

def compute_canonical(base):
    """Вычисляет каноническую форму ЗЛП"""
    a = base["A"]
    b = base["B"]
    c = base["C"]
    canonical_a1 = []
    for num in a[0]:
        canonical_a1.append(Rational(str(num  * sign(b[0]))))
    canonical_a1.append(Rational(str(sign(b[0]))))
    canonical_a1.append(Rational(str(0)))

    canonical_a2 = []
    for num in a[1]:
        canonical_a2.append(Rational(str(num * sign(b[1]))))
    canonical_a2.append(Rational(str(0)))
    canonical_a2.append(Rational(str(sign(b[1]))))

    canonical_b = []
    for num in b:
        canonical_b.append(Rational(str(abs(num))))

    canonical_c = [Rational(str(item)) for item in c[:]] + [Rational(str(0)), Rational(str(0))]

    canonical = {
        "A": [canonical_a1, canonical_a2],
        "B": canonical_b,
        "C": canonical_c,
    }
    return canonical
