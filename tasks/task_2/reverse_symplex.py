from util import deep_copy_matrix
from operations import recalculate_default
from sympy import Rational
def reverse_symplex_step(opt_table, opt_base, opt_free):
    if 'x5' in opt_free:
        remove_art_val(opt_table, opt_free)
    opt_base = var_names_to_indices(opt_base)
    opt_free = var_names_to_indices(opt_free)
    add_new_limitation(opt_table, opt_base)
    pseudo = deep_copy_matrix(opt_table)
    pseudo_base = opt_base[:]
    pseudo_free = opt_free[:]
    x_out = 4
    c_div_a = []
    for i in range(len(opt_free)):
        if opt_table[opt_base.index(x_out)][i] > 0:
            a = opt_table[opt_base.index(x_out)][i]
            c = opt_table[-1][i]
            c_div_a.append(-c/a)
        else:
            c_div_a.append(10000)
    x_in = c_div_a.index(min(c_div_a))
    opt_table = recalculate_default(opt_table, opt_base.index(x_out),x_in)
    opt_base[opt_base.index(x_out)] = opt_free[x_in]
    opt_free[x_in] = x_out
    return [(opt_table, var_indices_to_names(opt_base), var_indices_to_names(opt_free)),
            (pseudo, var_indices_to_names(pseudo_base), var_indices_to_names(pseudo_free))]
    
def remove_art_val(table, free):
    x5_col = free.index('x5')
    if len(table[0]) > 3:
        for row in table:
            del row[x5_col]
    del free[x5_col]

def var_names_to_indices(names):
    result = []
    for i in range(len(names)):
        # names[i] = int(names[i][1]) - 1
        result.append(int(names[i][1]) - 1)
    return result

def var_indices_to_names(indices):
    result = []
    for i in range(len(indices)):
        # indices[i] = f"x{indices[i]+1}"
        result.append(f"x{indices[i]+1}")
    return result

def add_new_limitation(table, base):
    row = -1
    if (0 in base):
        row = base.index(0)
    else:
        row = base.index(1)
    value = table[row][-1]
    if (value > 1):
        value -= 1
    elif (value > 0.25):
        value = Rational("0.25")
    else:
        value = 0
    
    new_table_row = [-item for item in table[row][:-1]] + [value - table[row][-1]]
    table.insert(2 ,new_table_row)
    base.append(4)