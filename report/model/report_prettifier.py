from sympy import Rational, primefactors, latex, Symbol, sign, Expr

from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem


def rational_latex(rational: Rational):
    if not isinstance(rational, Rational):
        return latex(rational)

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
            result = f"{num:.10f}".rstrip('0')
        else:
            if rational.p * rational.q < 0:
                op = " - "
            else:
                op = ""

            result = f"{op} \\frac{{{abs(rational.p)}}}{{{abs(rational.q)}}}"
    return result


def rational_coeff_term_latex(coeff: Rational, var: Symbol):
    result = ""
    match coeff:
        case 0:
            return result
        case 1:
            result = f"+ {latex(var)}"
        case -1:
            result = f"-{latex(var)}"
        case _:
            if coeff > 0:
                op = " + "
            else:
                op = ""
            coeff_latex = rational_latex(coeff)
            result = f"{op} {coeff_latex} {latex(var)}"
    return result


def expression_latex(coeffs: list[Rational | Expr], variables: list[Symbol], constant: Rational = Rational(0)):
    terms = []

    for coeff, var in zip(coeffs, variables):
        if isinstance(coeff, Rational):
            terms.append(rational_coeff_term_latex(coeff, var))
        elif isinstance(coeff, Expr):
            terms.append(f"{latex(coeff)}{latex(var)}")
        # Используем rational_latex для представления коэффициента

    # Добавляем константу, используя rational_latex
    constant_latex = rational_latex(constant)
    if constant != 0:
        if constant > 0:
            terms.append(f"+ {constant_latex}")
        else:
            terms.append(f"{constant_latex}")

    # Собираем все части в одну строку
    result = " ".join(terms)
    result = result.strip()
    result = result.lstrip("+")
    result = result.lstrip()
    # result = result.lstrip("+")
    # Убираем лишний плюс в начале выражения, если он есть
    # if result.startswith("+"):
    #     result = result[1:]
    #     # result = result.lstrip("+")

    return result
