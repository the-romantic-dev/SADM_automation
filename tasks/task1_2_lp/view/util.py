from sympy import latex, Eq, Expr


def eq_latex(left: Expr, right: Expr):
    return latex(Eq(left, right))
