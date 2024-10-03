from sympy import Rational, primefactors, latex, Symbol, sign, Expr, pretty, Add, Mul

from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem


def _rational_pretty(rational: Rational, frac_str: str):
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
            result = frac_str
    return result


def rational_str(rational: Rational):
    return _rational_pretty(rational, frac_str=str(rational))


def rational_latex(rational: Rational):
    if rational.p * rational.q < 0:
        op = " - "
    else:
        op = ""

    frac_str = f"{op} \\frac{{{abs(rational.p)}}}{{{abs(rational.q)}}}"
    return _rational_pretty(rational, frac_str=frac_str)


def coeff_with_symbol_latex(coeff: Expr):
    const = Rational(0)
    M_coeff = 0
    if isinstance(coeff, Add):
        for t in coeff.args:
            if isinstance(t, Rational):
                const += t
            elif isinstance(t, Symbol):
                M_coeff = 1
            elif isinstance(t, Mul):
                M_coeff = t.args[0]
    elif isinstance(coeff, Mul):
        M_coeff = coeff.args[0]
    return expr_latex(coeffs=[M_coeff], variables=[LPProblem.M], constant=const)


def _rational_coeff_term(coeff: Rational, var: Symbol | str, is_latex: bool):
    result = ""
    var_func = latex if is_latex else pretty
    if isinstance(var, str):
        def f(x): return x

        var_func = f
    match coeff:
        case 0:
            return result
        case 1:
            result = f"+ {var_func(var)}"
        case -1:
            result = f"-{var_func(var)}"
        case _:
            if coeff > 0:
                op = " + "
            else:
                op = ""

            if is_latex:
                coeff_latex = rational_latex(coeff)
                result = f"{op} {coeff_latex} {var_func(var)}"
            else:
                coeff_str = rational_str(coeff)
                result = f"{op} {coeff_str}·{var_func(var)}"
    return result


def _expression_pretty(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str], constant: Rational,
                       is_latex: bool):
    terms = []

    for coeff, var in zip(coeffs, variables):
        if isinstance(coeff, Rational):
            terms.append(_rational_coeff_term(coeff, var, is_latex))
        elif isinstance(coeff, float | int):
            terms.append(_rational_coeff_term(Rational(coeff), var, is_latex))
        elif isinstance(coeff, Expr):
            var_func = latex if is_latex else pretty
            if isinstance(var, str):
                def f(x): return x

                var_func = f
            if is_latex:
                terms.append(f"{latex(coeff)}{var_func(var)}")
            else:
                terms.append(f"{str(coeff)} · {var_func(var)}")

    constant_latex = rational_latex(constant)
    if constant != 0:
        if constant > 0:
            terms.append(f"+ {constant_latex}")
        else:
            terms.append(f"{constant_latex}")

    result = " ".join(terms)
    result = result.strip()
    result = result.lstrip("+")
    result = result.lstrip()

    return result


def expr_str(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str],
             constant: Rational = Rational(0)):
    return _expression_pretty(coeffs, variables, constant, is_latex=False)


def expr_latex(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str],
               constant: Rational = Rational(0)):
    return _expression_pretty(coeffs, variables, constant, is_latex=True)


def float_str(num: float, rounding: int):
    return f"{num:.{rounding}f}".rstrip('0').rstrip('.')
