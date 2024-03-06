# pylint: skip-file
from util import deep_copy_matrix, deep_copy_canonical, get_sign_symbol
from sympy import sympify, simplify, Rational, symbols

def recalculate_default(matrix, row, column):
    """Пересчитывает таблицу без искусственной переменной"""
    result = deep_copy_matrix(matrix)
    result[row][column] = 1
    for i in range(len(matrix)):
        if i != row:
            result[i][column] = matrix[i][column]
    
    for i in range(len(matrix[row])):
        if i != column:
            result[row][i] = -matrix[row][i]
    
    for i in range(len(matrix)):
        for j in range(len(matrix[row])):
            if (i != row) & (j != column):
                result[i][j] = matrix[i][j] * matrix[row][column] - matrix[row][j] * matrix[i][column]

    for i in range(len(matrix)):
        for j in range(len(matrix[row])):
            result[i][j] /= matrix[row][column]
    
    return result

def canonical_to_matrix(canonical):
    """Вычисляет начальную таблицу обычного симплекс метода"""
    row1 = [Rational(str(item)) * -1 for item in canonical["A"][0][0:2]] + [Rational(str(canonical["B"][0]))]
    row2 = [Rational(str(item)) * -Rational(str(canonical["A"][1][3])) for item in canonical["A"][1][0:2]] + [Rational(str(canonical["B"][1])) * Rational(str(canonical["A"][1][3]))]
    # row3 = canonical["C"] + [0.0]
    row3 = [Rational(str(item)) for item in canonical["C"]][0:2] + [Rational(str(0))]
    return [row1, row2, row3]

def canonical_to_artificial_var_form(canonical):
    result = deep_copy_canonical(canonical)
    M = symbols('M')
    result["C"] += [-M]
    result["A"][0] += [Rational(0)]
    result["A"][1] += [Rational(1)]
    return result

def artificial_var_form_to_matrix(artificial_var_form):
    x1x2x4_1 = artificial_var_form["A"][0][0:2] + [artificial_var_form["A"][0][3]]
    b_1 = artificial_var_form["B"][0]
    row1 = [Rational(str(i)) * -1 for i in x1x2x4_1] + [Rational(str(b_1))]
    
    x1x2x4_2 = artificial_var_form["A"][1][0:2] + [artificial_var_form["A"][1][3]]
    b_2 = artificial_var_form["B"][1]
    row2 = [Rational(str(i)) * -1  for i in x1x2x4_2] + [Rational(str(b_2))]
    
    x1x2x4_c = artificial_var_form["C"][0:2] + [artificial_var_form["C"][3]]
    row3 = []
    M = artificial_var_form["C"][4]
    for i in range(len(x1x2x4_c)):
        factor = Rational(str(x1x2x4_2[i]))
        const = Rational(str(x1x2x4_c[i]))
        row3.append(-factor * M + const)
    row3 += [Rational(str(b_2)) * M]
    return [row1, row2, row3]


