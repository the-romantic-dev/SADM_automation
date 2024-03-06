import sympy as sp
from task import Task
from scipy.optimize import minimize, linprog, minimize_scalar
import numpy as np


def gradient(X=None, expr=None):
    """Считает градиент. При наличии точки X считает градиент в точке"""
    x1, x2 = sp.symbols("x1 x2")
    f = Task.f
    if not expr is None:
        f = expr

    result = sp.Matrix([[sp.diff(f, x1)], [sp.diff(f, x2)]])
    if not X is None:
        result = result.subs({x1: X[0, 0], x2: X[1, 0]})
    return result


def gesse(X=None, expr=None):
    """Считает матрицу Гессе"""
    x1, x2 = sp.symbols("x1 x2")
    f = Task.f
    if not expr is None:
        f = expr
    result = sp.Matrix(
        [
            [sp.diff(f, x1, x1), sp.diff(f, x1, x2)],
            [sp.diff(f, x2, x1), sp.diff(f, x2, x2)],
        ]
    )
    if not X is None:
        result = result.subs({x1: X[0, 0], x2: X[1, 0]})
    return result


def default_step(X, K, expr=None):
    """Вычисление длины шага (t)"""
    a = gradient(X, expr).T * K
    b = K.T * gesse(X, expr) * K
    t_i = -a.det() / b.det()
    return t_i


def default_step_floated(X, K, expr=None):
    """Вычисление длины шага (t)"""
    a = gradient(X, expr).T.evalf() * K.evalf()
    b = K.T.evalf() * gesse(X, expr).evalf() * K.evalf()
    t_i = -a.det() / b.det()
    return t_i


def optimize(f, start):
    x1, x2 = sp.symbols("x1 x2")
    f_num = sp.lambdify([(x1, x2)], -f, "scipy")
    initial_guess = np.zeros(2)
    initial_guess[0] = start[0, 0]
    initial_guess[1] = start[1, 0]
    result = minimize(fun=f_num, x0=initial_guess, method="Nelder-Mead")
    return sp.Matrix(result["x"])


def optimize_linear(f: sp.Expr, limits):
    coef_map = (-f).as_coefficients_dict()
    vars_tuple = tuple(coef_map.keys())[::-1]
    C = [coef_map[x] for x in vars_tuple]
    A, b = sp.linear_eq_to_matrix(limits, vars_tuple)
    result = linprog(c=C, A_ub=A.tolist(), b_ub=b.tolist(), method="highs")
    return sp.Matrix(list(result.x))


def univariate_step(X, K, f=None, start_interval: list = [0, 1]) -> float:

    if f is None:
        f = Task.f
    x1, x2, t = sp.symbols("x1 x2 t")
    
    solution = X + t * K
    value = f.subs({x1: solution[0,0], x2: solution[1,0]})
    func = sp.lambdify(t, -value, 'numpy')
    return minimize_scalar(fun=func,bracket=start_interval, method='golden').x

def univariate_step_my(X, K, f=None) -> float:
    tol = 1e-3
    golden = 1.618
    if f is None:
        f = Task.f
    x1, x2, t = sp.symbols("x1 x2 t")
    solution = X + t * K
    value = f.subs({x1: solution[0,0], x2: solution[1,0]})
    
    def undefined_interval():
        t0 = 0
        t1 = 1
        f0 = value.subs({t: t0})
        f1 = value.subs({t: t1})
        while True:
            t2 = t1 + 1.62 * (t1 - t0)
            f2 = value.subs({t: t2})
            if f2 < f1:
                break
            f0 = f1
            f1 = f2
            t0 = t1
            t1 = t2
        return [t0, t2]
        
    def step(a,b):
        x_1 = b - (b-a)/golden
        x_2 = a + (b-a)/golden
        y_1 = value.subs({t: x_1})
        y_2 = value.subs({t: x_2})
        if y_1 <= y_2:
            a = x_1
        else:
            b= x_2
        return a,b
    
    a,b = undefined_interval()
    while abs(a - b) >= tol:
        a,b = step(a,b)
    return (a+b)/2


def delete_matrix_columns(matrix, index_start, index_end):
    return matrix[:,:index_start-1].row_join(matrix[:,index_end:])

def recalculate_symplex_table(table, opt_col, opt_row):
    """Пересчитывает симплекс таблицу
    
    ### Формат таблицы
    - без заголовочных переменных
    - без столбца b/x
    - со строкой f
    """
    result = [
        [0 for _, _ in enumerate(table[0])] for i, _ in enumerate(table)
    ]
    result[opt_row][opt_col] = 1

    for i, _ in enumerate(result):
        if i != opt_row:
            result[i][opt_col] = table[i][opt_col]

    for j, _ in enumerate(result[0]):
        if j != opt_col:
            result[opt_row][j] = -table[opt_row][j]

    for i, _ in enumerate(result):
        for j, _ in enumerate(result[0]):
            if i != opt_row and j != opt_col:
                main_diag = table[opt_row][opt_col] * table[i][j]
                second_diag = table[i][opt_col] * table[opt_row][j]
                result[i][j] = main_diag - second_diag
    for i, _ in enumerate(result):
        for j, _ in enumerate(result[0]):
                result[i][j] /= table[opt_row][opt_col]
    return result

def is_X_allowed(X, limitations, type = 'le'):
    """type:
        -le, -ge, -eq"""
    x1,x2 = sp.symbols('x1 x2')
    result = True
    for lim in limitations:
        sol = lim.subs({x1: X[0,0], x2: X[1,0]})
        match type:
            case 'le':
                if sol > 0:
                    result = False
                    break
            case 'ge':
                if sol < 0:
                    result = False
                    break
            case 'eq':
                if sol != 0:
                    result = False
                    break
    return result

def merge_symplex_table_and_vars(symplex_table, free, base):
    result = [row.copy() for row in symplex_table]
    for row_index in range(len(base)):
        result[row_index] = [base[row_index]] + result[row_index]
    
    result = [['-'] + free + ['b']] + result
    return result

