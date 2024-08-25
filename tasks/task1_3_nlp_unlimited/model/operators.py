"""Набор нужных математических функций"""
# import sympy as sp
#
#
# def gradient(expr, variables):
#     """Считает градиент"""
#     return [sp.diff(expr, x) for x in variables]


def def_gradient(expr, x1_val, x2_val):
    return [item.subs({
        x1: x1_val,
        x2: x2_val}) for item in gradient(expr)]


def gesse(expr_or_grad):
    """Считает матрицу Гессе"""
    grad = expr_or_grad
    if isinstance(expr_or_grad, sp.core.add.Add):
        grad = gradient(expr_or_grad)
    elif isinstance(expr_or_grad, list):
        grad = expr_or_grad
    else:
        return -1
    return [[sp.diff(grad[0], x1), sp.diff(grad[0], x2)],
            [sp.diff(grad[1], x1), sp.diff(grad[1], x2)]]


def step_size(expr, k, x_i):
    grad = gradient(expr)
    grad[0] = grad[0].subs({x1: x_i[0, 0], x2: x_i[1, 0]})
    grad[1] = grad[1].subs({x1: x_i[0, 0], x2: x_i[1, 0]})
    grad = sp.Matrix(grad)
    ges = sp.Matrix(gesse(expr))

    a = grad.T * k
    b = k.T * ges * k
    t_i = -a.det() / b.det()
    return t_i
