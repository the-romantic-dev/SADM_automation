from sympy import symbols, Expr
import sympy as sp

def default_symplex_method_next_step(matrix):
    """Вычисляет симплекс метод"""

    if matrix[0][-1] < 0 or matrix[1][-1] < 0:
        raise ValueError("недопустимый базис")

    is_opt = True
    M = symbols("M")
    for c in matrix[-1][:-1]:
        if isinstance(c, Expr):
            c = c.subs(M, 1000)
        if c > 0:
            is_opt = False
            break

    if not is_opt:
        column = matrix[-1][:-1].index(max(matrix[-1][:-1], key=lambda c: c.subs(M, 1000)))
        row = -1
        b_div_a = []
        for cur_row in matrix[:-1]:
            b_div_a.append(cur_row[-1] / cur_row[column])

        neg_b_div_a = [x for x in b_div_a if x < 0]
        row = b_div_a.index(min(neg_b_div_a, key=lambda x: abs(x)))
        return [row, column]
    else:
        return [-1, -1]

def matrix_symplex_method_next_step(canonical, base=[2,3]):
    A = sp.Matrix(canonical['A'])
    B = sp.Matrix(canonical['B'])
    C = sp.Matrix(canonical['C'])
    based_C = sp.Matrix([C[base[0]], C[base[1]]])

    P = sp.Matrix([[A[0,base[0]], A[0,base[1]]], [A[1,base[0]], A[1,base[1]]]])
    P_inv = P.inv()
    F = based_C.T * P_inv * B
    Deltas = []
    for i in range(C.rows):
        if i in base:
            Deltas.append("based")
        else:
            delta = based_C.T * P_inv * A[:, i] - C[i, :]
            Deltas.append(delta)
    base_sol_X =  P_inv * B
    m = symbols('M')
    min_delta = min([item for item in Deltas if not isinstance(item, str)], key=lambda d: d.det().subs(m,1000))
    x_div_z_1 = "opt"
    x_div_z_2 = "opt"
    x_in = "opt"
    x_out = "opt"
    Z = "opt"

    if min_delta.det().subs(m, 1000) < 0:
        x_in = Deltas.index(min_delta)
        Z = P_inv * A[:, x_in]
        x_div_z_1 = base_sol_X[0,0] / Z[0, 0]
        x_div_z_2 = base_sol_X[1,0] / Z[1, 0]
        x_out = -1
        if Z[0, 0] > 0 and Z[1, 0] > 0:
            x_out = base[0] if x_div_z_1 <= x_div_z_2 else base[1]
        elif Z[0, 0] < 0:
            x_out = base[1]
        else:
            x_out = base[0]

    return {
        "A": A,
        "P": P,
        "P_inv": P_inv,
        "F": F,
        "Deltas": [item.det() if not isinstance(item, str) else item for item in Deltas],
        "x_out": x_out,
        "x_in": x_in,
        "Z": Z,
        "base_sol_X": base_sol_X,
        "x_div_z_1": x_div_z_1,
        "x_div_z_2": x_div_z_2,
        "based_C": based_C
    }
        