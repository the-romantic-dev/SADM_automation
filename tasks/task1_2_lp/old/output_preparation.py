# pylint: skip-file
from tabulate import tabulate
from file import add_output
from sympy import symbols

def tabulate_matrix(base, free, matrix):
    """ Представляет вычисленную симплекс таблицу в виде матрицы"""
    row_headers = base + ["f"]
    col_headers = free + ["b"]
    
    str_matrix = [[rational_to_str(item) for item in row] for row in matrix]
    new_matrix = [row_headers[i:i+1] + row for i, row in enumerate(str_matrix)]
    table = tabulate(new_matrix, col_headers, tablefmt="grid", colalign=("center", "center", "center", "center"))
    add_output(f"Базис: {base[0]}, {base[1]}\n" + table + "\n")

def row_to_equation(coefficients=[], eq="", var='x'):
    x = []
    expr = 0
    for i in range(len(coefficients)):
        x.append(symbols(f'{var}{i+1}'))
        expr += coefficients[i] * x[i]
    
    result = str(expr)
    
    if len(str(eq)) > 0:
        result += f" = {eq}"

    return result

def rational_to_str(rational):
    result = str(rational)
    try:
        q = rational.q
        p = rational.p
    except Exception as e:
        return result
    
    if is_rational_finite_decimal(q):
        result = str(float(rational))
    elif (abs(p) >= abs(q)):
        # quotient, remainder = divmod(rational, 1)
        result = f"{int(rational)}${abs(rational - int(rational))}"
    return result

def is_rational_finite_decimal(q):
    # Проверяем, является ли знаменатель степенью 2 или 5
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5

    # Если знаменатель равен 1, то дробь конечная
    return q == 1