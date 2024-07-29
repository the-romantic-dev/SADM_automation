from sympy import symbols, Expr, Float, Rational, Number, Integer, primefactors


def get_non_negative_vars_latex(vars_count: int):
    result = [f"x_{i + 1} \\ge 0" for i in range(vars_count)]
    return ",".join(result)





