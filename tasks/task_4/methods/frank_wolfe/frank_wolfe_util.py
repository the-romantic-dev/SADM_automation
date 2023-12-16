from sympy import Matrix, eye, zeros, symbols, diff
from util import gradient, gesse, delete_matrix_columns

x1, x2 = symbols("x1 x2")
v1, v2, lambda1, lambda2, y1, y2, k1, k2 = symbols("v1 v2 λ1 λ2 y1 y2 k1 k2")


def build_quadratic_form_matrices(expr):
    """Из выражения строит матрицы-коэффициенты его квадратичной формы"""
    zero = Matrix([0, 0])
    p = gradient(X=zero, expr=expr)
    H = gesse(X=zero, expr=expr)
    return p, H


def build_AEOO_HOOEAT(A, H):
    E = eye(2)
    O = zeros(2)
    row1 = A.row_join(E).row_join(O).row_join(O)
    row2 = H.row_join(O).row_join(E).row_join(-A.T)
    return row1.col_join(row2)


def build_bp(b, p):
    return b.col_join(-p)


def build_frank_wolfe_limits_matrix(A, b, H, p):
    """Из матриц задачи квадратичного программирования
    строит матрицы ограничений метода Франка-Вульфа"""
    # E = eye(2)
    # O = zeros(2)
    # left_row1 = A.row_join(E).row_join(O).row_join(O)
    # left_row2 = H.row_join(O).row_join(E).row_join(-A.T)
    left_row2 = -left_row2
    left = left_row1.col_join(left_row2)
    K = O.col_join(E)
    left = left.row_join(K)
    right = b.col_join(-(-p))
    return left, right


def build_kk_symplex_table(AEOO_HOEAT, bp):
    """Строит начальную симплекс-таблицу для метода Франка-Вульфа"""
    E = eye(2)
    O = zeros(2)
    K = O.col_join(E)
    AEOO_HOEAT: Matrix = AEOO_HOEAT.copy()
    bp: Matrix = bp.copy()

    AEOO_HOEAT.row_op(2, lambda v, j: -v)
    AEOO_HOEAT.row_op(3, lambda v, j: -v)
    bp.row_op(2, lambda v, j: -v)
    bp.row_op(3, lambda v, j: -v)

    AEOO_HOEAT = AEOO_HOEAT.row_join(K)

    # AEOO_HOEAT = -delete_matrix_columns(
    #     delete_matrix_columns(AEOO_HOEAT, 9, 10), 3, 4
    # )

    AEOO_HOEAT.col_del(9)
    AEOO_HOEAT.col_del(8)
    AEOO_HOEAT.col_del(3)
    AEOO_HOEAT.col_del(2)

    AEOO_HOEAT = -AEOO_HOEAT

    result = AEOO_HOEAT.row_join(bp)
    expr_row = Matrix([-row[2] - row[3] for row in result.T.tolist()]).T
    return result.col_join(expr_row).tolist()


def build_fw_symplex_table(kk_free, base, kk_symplex_table, Z, tilda_Z_0):
    """Строит начальную симплекс-таблицу для метода Франка-Вульфа"""
    result = [row.copy() for row in kk_symplex_table]
    del result[-1]
    for row in result:
        for i in reversed(list(range(len(row) - 1))):
            if kk_free[i] == k1 or kk_free[i] == k2:
                del row[i]
    free = kk_free.copy()
    free.remove(k1)
    free.remove(k2)
    ZZ = (Z.T * tilda_Z_0).det()
    if ZZ != 0:
        Z_vars = [x1, x2, y1, y2, v1, v2, lambda1, lambda2]
        func_row = [diff(ZZ, var) for var in free]
        func_row.append(ZZ.subs({var: 0 for var in Z_vars}))
        result.append(func_row)
    else:
        func_row= []
        b_col = [result[i][-1] for i in range(len(result))]
        tilda_vars = (v1, v2, lambda1, lambda2, x1, x2, y1, y2)
        not_tilda_vars = (x1, x2, y1, y2, v1, v2, lambda1, lambda2)
        for i in free:
            pair = tilda_vars[not_tilda_vars.index(i)]
            func_row.append(b_col[base.index(pair)])
        func_row += [0]
        result.append(func_row)
    return result, free


def find_opt_column_and_row(table, isMax=True):
    """Находит оптимальные столбец и строку в симплекс-таблице"""
    opt_col = None
    if isMax:
        opt_col = table[-1].index(max(table[-1][:-1]))
    else:
        opt_col = table[-1].index(min(table[-1][:-1]))
    row_criteria = [-row[-1] / row[opt_col] for row in table[:-1]]
    for i in range(len(row_criteria)):
        if table[:-1][i][opt_col] == 0 or row_criteria[i] < 0:
            row_criteria[i] = 1e10
    opt_row = row_criteria.index(min(row_criteria))
    return opt_col, opt_row


def is_symplex_table_opt(table, isMax=True):
    """Проверяет, является ли текущая симплекс-таблица оптимальной"""
    result = True
    for coef in table[-1][:-1]:
        if (isMax and coef > 0) or (not isMax and coef <= 0):
            result = False
            break
    return result


def recalculate_base_and_free(base, free, opt_col, opt_row):
    """Пересчитывает списки базисных и свободных переменных"""
    base = base.copy()
    free = free.copy()
    t = base[opt_row]
    base[opt_row] = free[opt_col]
    free[opt_col] = t
    return base, free


def get_current_point(symplex_table, free, base):
    X = []
    if symbols('x1') in free:
        X.append(0)
    else:
        X.append(symplex_table[base.index(symbols('x1'))][-1])

    if symbols('x2') in free:
        X.append(0)
    else:
        X.append(symplex_table[base.index(symbols('x2'))][-1])
    return Matrix(X)


def build_Z_expr(kk_symplex_table, free, base):
    Z_vars = (x1, x2, y1, y2, v1, v2, lambda1, lambda2)
    Z = [0 for i in Z_vars]
    table_copy = [row.copy() for row in kk_symplex_table]
    del table_copy[-1]
    for i, row in enumerate(table_copy):
        expr = 0
        for j in range(len(row)):
            if j < len(free):
                if free[j] != k1 and free[j] != k2:
                    expr += row[j] * free[j]
            else:
                expr += row[j]
        Z_var_index = Z_vars.index(base[i])
        Z[Z_var_index] = expr
    return Matrix(Z)


def build_Z(kk_symplex_table, base, is_tilda=True):
    if is_tilda:
        result_vars = (v1, v2, lambda1, lambda2, x1, x2, y1, y2)
    else:
        result_vars = (x1, x2, y1, y2, v1, v2, lambda1, lambda2)

    result = [0 for i in result_vars]
    table_copy = [row.copy() for row in kk_symplex_table]
    del table_copy[-1]
    for i, row in enumerate(table_copy):
        const = row[-1]
        var_index = result_vars.index(base[i])
        result[var_index] = const
    return Matrix(result)


def rebuild_fw_symplex_table(free, base, new_Z_expr, new_Z):
    tilda_vars = (v1, v2, lambda1, lambda2, x1, x2, y1, y2)
    not_tilda_vars = (x1, x2, y1, y2, v1, v2, lambda1, lambda2)
    result = []
    for i in range(len(base)):
        result.append([])
        for var_free in free:
            result[i].append(diff(new_Z_expr[not_tilda_vars.index(base[i]), 0], var_free))
    new_Z_tilda = Z2tilda_Z(new_Z)
    expr = (new_Z_expr.T * new_Z_tilda).det()
    b_col = [new_Z_expr[not_tilda_vars.index(var), 0].subs({fv: 0 for fv in free}) for var in base]
    for i in range(len(b_col)):
        result[i].append(b_col[i])
    if (expr == 0):
        expr_row = []
        for i in free:
            pair = tilda_vars[not_tilda_vars.index(i)]
            expr_row.append(b_col[base.index(pair)])
        expr_row += [0]
        result.append(expr_row)
    else:
        expr_row = []
        for i in free:
            expr_row.append(diff(expr, i))
        expr_row.append(expr.subs({i:0 for i in free}))
        result.append(expr_row)
    return result


def Z2tilda_Z(Z):
    if isinstance(Z, Matrix):
        Z = Z.tolist()
    tilda_vars = (v1, v2, lambda1, lambda2, x1, x2, y1, y2)
    not_tilda_vars = (x1, x2, y1, y2, v1, v2, lambda1, lambda2)
    vars_dict = {not_tilda_vars[i]: Z[i] for i in range(len(Z))}
    result = []
    for i in tilda_vars:
        result.append(vars_dict[i])
    return Matrix(result)
