"""Файл со вспомогательными функциями для решения методом Била
(их реально дохуя, я запутался, поэтому в другой файл вынес)"""
from sympy import symbols, linear_eq_to_matrix,diff, Matrix, Rational, solve
from sympy.core.numbers import ComplexInfinity


def gag_fix(x, limitations):
    """Если в ограничении x1>=b, b не равен нулю, то делаем замену переменной,
    чтобы это было так"""
    if limitations[2].subs({x[0]: 0}) != 0:
        const = limitations[2].subs({x[0]: 0})
        y1 = symbols("y1")
        limitations[2] = limitations[2].subs({x[0]: y1 + const})
        x[0] = y1

def is_opt(table1):
    """Проверяет, найдена ли оптимальная точка"""
    result = True
    for grad in table1[-1]:
        if grad > 0:
            result = False
            break
    return result

def build_start_table(x, limitations, expr) -> list:
    """Формирует начальную таблицу"""
    free = x[:2]
    base = x[2:]
    result = []

    a, b = linear_eq_to_matrix(limitations[:2], free)
    result += (-a).row_join(b).tolist()

    grads = []
    for xi in free:
        grads.append(diff(expr, xi))
    result.append(grads)

    def_grads = Matrix(grads)
    for xi in free:
        def_grads = def_grads.subs({xi: 0})
    result.append(def_grads.T.tolist()[0])

    return result, free, base

u = []
def build_table_2(table1, free):
    """Строит таблицу 2 на основе таблицы 1"""
    # u.append(symbols(f"u{len(u)+1}"))
    opt_col = opt_column(table1)
    half_grad = Rational('1/2') * table1[-2][opt_col]
    u_coefs = []

    for var in free:
        coef = diff(half_grad, var)
        u_coefs.append(Rational(coef))

    u_value = half_grad.subs({var: 0 for var in free})
    u_coefs.append(Rational(u_value))
    u.append(symbols(f"u{len(u)+1}"))
    table2 = table1[ : len(table1) - 2] + [u_coefs]
    return table2, opt_col, half_grad

def opt_column(table1):
    """Находит оптимальный столбец в таблице 1 (с градиентами)"""
    opt = 0
    for col,_ in enumerate(table1[-1]):
        if table1[-1][col] > table1[-1][opt]:
            opt = col
    return opt

def find_opt_row(table2, opt_col):
    """Находит оптимальную строку в таблице 2 (с новой переменной u)"""
    permission_column = [-row[-1] / row[opt_col] for row in table2]
    for i in range(len(permission_column)):
        if isinstance(permission_column[i], ComplexInfinity):
            permission_column[i] = 0
    opt_row = permission_column.index(max(permission_column))
    for i, _ in enumerate(permission_column):
        if permission_column[i] > 0 and permission_column[i] < permission_column[opt_row]:
            opt_row = i
    return opt_row

def transition_to_new_base(base, free, opt_row, opt_col):
    """Переход в новый базис"""
    base = base.copy()
    free = free.copy()
    temp = base[opt_row]
    base[opt_row] = free[opt_col]
    free[opt_col] = temp
    return free, base

def build_table_1(table2, opt_col, free, base, expr) -> list:
    """Строит таблицу 1"""
    table2 = [row.copy() for row in table2]
    base = base.copy()
    free = free.copy()
    opt_row = find_opt_row(table2=table2, opt_col=opt_col)
    if opt_row == len(table2) - 1:
        # new_u = symbols(f'u{len(u)+1}')
        # u.append(new_u)
        base += [u[-1]]
    else:
        del table2[-1]
    new_expr = recalculate_expression(expr, free, base, table2, opt_row, opt_col)
    free, base = transition_to_new_base(free=free, base=base, opt_row=opt_row, opt_col=opt_col)
    result = recalculate_table2(table2=table2, opt_row=opt_row, opt_col=opt_col)
    grads = []
    for xi in free:
        grads.append(diff(new_expr, xi))
    result.append(grads)

    def_grads = Matrix(grads)
    for xi in free:
        def_grads = def_grads.subs({xi: 0})
    result.append(def_grads.T.tolist()[0])

    return result, free, base, new_expr, opt_row

def recalculate_expression(expr, free, base, table2, opt_row, opt_col):
    """Перечитывает выражение после замены переменных"""
    var_out_of_free = free[opt_col]
    var_out_of_base = base[opt_row]
    new_var_expr = table2[opt_row][0] * free[0] + table2[opt_row][1] * free[1] +  table2[opt_row][2]
    new_var_in_expr = solve(new_var_expr - var_out_of_base, var_out_of_free)[0]
    new_expr = expr.subs({var_out_of_free: new_var_in_expr}).simplify()
    return new_expr

def recalculate_table2(table2, opt_row, opt_col):
    """Пересчитывает таблицу 2"""
    result = [
        [0 for _, _ in enumerate(table2[0])] for i, _ in enumerate(table2)
    ]
    result[opt_row][opt_col] = 1

    for i, _ in enumerate(result):
        if i != opt_row:
            result[i][opt_col] = table2[i][opt_col]

    for j, _ in enumerate(result[0]):
        if j != opt_col:
            result[opt_row][j] = -table2[opt_row][j]

    for i, _ in enumerate(result):
        for j, _ in enumerate(result[0]):
            if i != opt_row and j != opt_col:
                main_diag = table2[opt_row][opt_col] * table2[i][j]
                second_diag = table2[i][opt_col] * table2[opt_row][j]
                result[i][j] = main_diag - second_diag
    for i, _ in enumerate(result):
        for j, _ in enumerate(result[0]):
                result[i][j] /= table2[opt_row][opt_col]
    return result
