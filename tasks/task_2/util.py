# pylint: skip-file
from sympy import symbols

def deep_copy_matrix(matrix):
    result = []
    for row in matrix:
        result.append(row[:])
    return result

def deep_copy_canonical(canonical):
    result = {
        "A":[canonical["A"][0][:], canonical["A"][1][:]],
        "B":canonical["B"][:],
        "C":canonical["C"][:]
    }
    return result
    

def get_sign_symbol(num):
    result = ""
    if num >= 0:
        result = "+"
    elif num < 0:
        result = "-"
    return result

def is_all_deltas_positive(list):
    result = True
    m = symbols('M')
    for i in list:
        if isinstance(i, str):
            continue
        if i.subs(m, 1000) < 0:
            result = False
            break
    return result