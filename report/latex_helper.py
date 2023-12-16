from sympy import latex, symbols, Eq, Le, Ge


x1, x2 = symbols('x1 x2')


def latex_max(sympy_or_latex_expr):
    result = None
    if isinstance(sympy_or_latex_expr, str):
        result = f'\\max\\left({sympy_or_latex_expr}\\right)'
    else:
        result = f'\\max\\left({latex(sympy_or_latex_expr)}\\right)'
    return result


def latex_limit(limit, lim_type='le'):
    free_coef = -limit.subs({x1: 0, x2: 0})
    limit = limit + free_coef
    result = None
    match lim_type:
        case 'eq':
            result = Eq(limit, free_coef)
        case 'le':
            result = Le(limit, free_coef)
        case 'ge':
            result = Ge(limit, free_coef)
        case _:
            raise ValueError(f'Неверный аргумент lim_type={lim_type}')
    return latex(result)


def latex_expr_degree_decision(sympy_expr):
    coefs = sympy_expr.as_coefficients_dict()
    order = [x1 ** 2, x2 ** 2, x1 * x2, x1, x2]
    result = ''
    for elem in order:
        sign = None
        if coefs[elem] > 0:
            sign = '+'
        elif coefs[elem] < 0:
            sign = '-'
        if result != 0 or sign == '-':
            result += f' {sign} '
        result += latex(abs(coefs[elem]) * elem)
    return result
