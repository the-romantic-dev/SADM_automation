from sympy import Rational, primefactors, latex, Symbol


def rational_latex(rational: Rational):
    def is_finite_float():
        q_prime_factors = set(primefactors(rational.q))
        for factor in q_prime_factors:
            if factor not in [2, 5]:
                return False
        return True

    if rational.q == 1:
        result = str(rational.p)
    else:
        if is_finite_float():
            num = float(rational)
            result = f"{num:.15f}".rstrip('0')
        else:
            result = f"\\frac{{{rational.p}}}{{{rational.q}}}"
    return result


def expression_latex(coeffs: list[Rational], variables: list[Symbol], constant: Rational = Rational(0)):
    # Создаем список частей выражения
    terms = []

    for coeff, var in zip(coeffs, variables):
        # Используем rational_latex для представления коэффициента
        if coeff == 0:
            continue
        coeff_latex = rational_latex(coeff)

        # Если коэффициент равен 1, не отображаем его
        if coeff == 1:
            terms.append(f"+ {latex(var)}")
        # Если коэффициент равен -1, отображаем только минус
        elif coeff == -1:
            terms.append(f"-{latex(var)}")
        else:
            terms.append(f"+ {coeff_latex} {latex(var)}")

    # Добавляем константу, используя rational_latex
    constant_latex = rational_latex(constant)
    if constant != 0:
        if constant > 0:
            terms.append(f"+ {constant_latex}")
        else:
            terms.append(f"{constant_latex}")

    # Собираем все части в одну строку
    result = " ".join(terms)

    # Убираем лишний плюс в начале выражения, если он есть
    if result.startswith("+ "):
        result = result[2:]

    return result

# class PrettyRational:
#     def __init__(self, rational: Rational):
#         self.rational = rational
#
#     @property
#     def is_finite_float(self):
#         q_prime_factors = set(primefactors(self.rational.q))
#         for factor in q_prime_factors:
#             if factor not in [2, 5]:
#                 return False
#         return True
#
#     @property
#     def latex(self) -> str:
#         if self.rational.q == 1:
#             return str(self.rational.p)
#         else:
#             if self.is_finite_float:
#                 num = float(self.rational)
#                 return f"{num:.15f}".rstrip('0')
#             else:
#                 return f"\\frac{{{self.rational.p}}}{{{self.rational.q}}}"
