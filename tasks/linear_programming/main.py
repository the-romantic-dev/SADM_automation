# pylint: skip-file
"""Главный отчет"""

from file import read_input, add_output, clear_output
from canonical_form import compute_canonical
from output_preparation import tabulate_matrix, row_to_equation
from operations import (
    recalculate_default,
    canonical_to_matrix,
    canonical_to_artificial_var_form,
    artificial_var_form_to_matrix
)
from symplex_method import default_symplex_method_next_step, matrix_symplex_method_next_step
from tasks.linear_programming.util import is_all_deltas_positive
from reverse_symplex import reverse_symplex_step, var_names_to_indices
from reverse_task import reverse_canonical, conjugate_points
from sympy import sympify, symbols

def add_output_expressions(dict):
    add_output(f"max({row_to_equation(dict['C'])})")
    add_output(f"{row_to_equation(dict['A'][0], dict['B'][0])}")
    add_output(f"{row_to_equation(dict['A'][1], dict['B'][1])}")
    odz = ""
    for i in range(len(dict['A'][0])):
        if (i != len(dict['A'][0])-1):
            odz += f"x{i+1}>=0, "
        else:
            odz += f"x{i+1}>=0"
    add_output(odz)

def add_output_reverse_task(dict):
    add_output(f"min({row_to_equation(dict['C'], var='y')})")
    for i in range(len(dict['A'])):
        add_output(f"{row_to_equation(dict['A'][i], var='y')} >= {str(dict['B'][i])}")

def add_output_all_bases():
    s1 = canonical_to_matrix(canonical)
    tabulate_matrix(base=["x3", "x4"], free=["x1", "x2"], matrix=s1)

    s2 = recalculate_default(s1, 0, 1)
    tabulate_matrix(base=["x2", "x4"], free=["x1", "x3"], matrix=s2)

    s3 = recalculate_default(s2, 1, 1)
    tabulate_matrix(base=["x2", "x3"], free=["x1", "x4"], matrix=s3)

    s4 = recalculate_default(s3, 0, 0)
    tabulate_matrix(base=["x1", "x3"], free=["x2", "x4"], matrix=s4)

    s5 = recalculate_default(s4, 1, 1)
    tabulate_matrix(base=["x1", "x4"], free=["x2", "x3"], matrix=s5)

    s6 = recalculate_default(s5, 1, 0)
    tabulate_matrix(base=["x1", "x2"], free=["x4", "x3"], matrix=s6)


def add_output_table_default_symplex():
    matrix = canonical_to_matrix(canonical)
    base = ["x3", "x4"]
    free = ["x1", "x2"]
    tabulate_matrix(base, free, matrix)
    swap = default_symplex_method_next_step(matrix)
    while swap[0] >= 0 and swap[1] >= 0:
        matrix = recalculate_default(matrix, swap[0], swap[1])

        buffer = base[swap[0]]
        base[swap[0]] = free[swap[1]]
        free[swap[1]] = buffer

        tabulate_matrix(base, free, matrix)

        swap = default_symplex_method_next_step(matrix)
    return matrix, base, free

def add_output_table_artificial_var_symplex(artificial_var_form):
    matrix = artificial_var_form_to_matrix(artificial_var_form)
    base = ["x3", "x5"]
    free = ["x1", "x2", "x4"]
    tabulate_matrix(base, free, matrix)
    swap = default_symplex_method_next_step(matrix)
    while swap[0] >= 0 and swap[1] >= 0:
        matrix = recalculate_default(matrix, swap[0], swap[1])

        buffer = base[swap[0]]
        base[swap[0]] = free[swap[1]]
        free[swap[1]] = buffer

        tabulate_matrix(base, free, matrix)

        swap = default_symplex_method_next_step(matrix)
    return matrix, base, free

def add_output_matrix_symplex(canonical, start_base):
    # result = matrix_symplex_method_next_step(canonical, start_base)
    counter = 0
    base = start_base[:]
    free = [i for i in range(len(canonical['C'])) if not i in start_base]
    # matrix_simplex_step_output(matrix_data=result, counter=counter, free=free, base=base)
    B = canonical['B']
    
    is_opt = False

    while not is_opt:
        result = matrix_symplex_method_next_step(canonical, base)
        is_opt = is_all_deltas_positive(result['Deltas'])
        matrix_simplex_step_output(matrix_data=result, counter=counter, free=free, base=base, is_opt=is_opt, B=B)
        if is_opt:
            break
        x_in = result['x_in']
        x_out = result['x_out']
        base.remove(x_out)
        base.append(x_in)
        free.remove(x_in)
        free.append(x_out)
        counter += 1
        

def matrix_simplex_step_output(matrix_data, counter, free, base, is_opt, B):
    P = matrix_data['P'].tolist()
    P_inv = matrix_data['P_inv'].tolist()
    based_CT = matrix_data['based_C'].T.tolist()
    # B = matrix_data['B'].tolist()
    F = matrix_data['F'].det()
    add_output(f"\nБазис x{base[0] + 1} x{base[1] + 1}")
    add_output(f"P{counter}:{P}")
    add_output(f"P{counter}_inv:{P_inv}")
    add_output(f"F = C^TБ{counter} * P{counter}^-1 * B = {based_CT} * {P_inv} * {B} = {F}")
    for i in free:
        add_output(f"Δ{i+1} = C^TБ{counter} * P{counter}^-1 * A{i+1} - c{i+1} = {based_CT} * {P_inv} * {matrix_data['A'][:, i].tolist()} = {matrix_data['Deltas'][i]}")
    
    if not is_opt:
        x_in = matrix_data['x_in']
        add_output(f"В базис входит x{x_in}")
        Z = matrix_data['Z'].tolist()
        add_output(f"Z{x_in + 1} = P{counter}^-1 * A{x_in + 1} = {Z}")
    else:
        for i in free:
            add_output(f"Δ{i+1} >= 0")
        add_output("-> Это оптимальная точка")
    base_sol_X = matrix_data['base_sol_X'].tolist()
    add_output(f"~X^Б{counter} = P{counter}^-1 * B = {base_sol_X}")
    
    if not is_opt:
        for i in range(len(base)):
            add_output(f"~x{base[i] + 1}^Б{counter} / z{i+1} = {matrix_data[f'x_div_z_{i+1}']}")
        x_out = matrix_data['x_out']
        add_output(f"Из базиса выходит x{x_out + 1}")

clear_output()

A1, A2, B, C, teacher = read_input()
base = {"A": [A1, A2], "B": B, "C": C}
canonical = compute_canonical(base)
add_output("1. Каноническая форма:")
add_output_expressions(canonical)
add_output("\n2. Метод перебора:")
add_output_all_bases()
add_output("\n3. Табличный симплекс:")
opt_table = []
base = []
free = []
if canonical["A"][1][3] == -1:
    artificial_var_form = canonical_to_artificial_var_form(canonical)
    matrix = artificial_var_form_to_matrix(artificial_var_form)
    add_output_expressions(artificial_var_form)
    add_output("")
    opt_table, base, free = add_output_table_artificial_var_symplex(artificial_var_form)
    add_output("")
    add_output("\n4. Матричный симплекс:")
    add_output_matrix_symplex(artificial_var_form, [2,4])
else:
    opt_table, base, free = add_output_table_default_symplex()
    add_output("\n4. Матричный симплекс:")
    add_output_matrix_symplex(canonical, [2,3])

add_output("\n5. Двойственный симплекс:")
reverse_symplex_result = reverse_symplex_step(opt_table, base, free)
pseudo_table, pseudo_base, pseudo_free = reverse_symplex_result[1]
new_opt_table, new_opt_base, new_opt_free = reverse_symplex_result[0]
add_output("\nПсевдоплан:")
tabulate_matrix(pseudo_base, pseudo_free, pseudo_table)
add_output("\nНовая оптимальная точка:")
tabulate_matrix(new_opt_base, new_opt_free, new_opt_table)

add_output("\n6. Двойственная задача:")
add_output("\nИсходная:")
add_output_expressions(canonical)
add_output("\nДвойственная:")
reversed_canonical = reverse_canonical(canonical=canonical)
add_output_reverse_task(reversed_canonical)

conjugate_result = conjugate_points(base=var_names_to_indices(base), canonical = canonical)
add_output("Найдем сопряженную точку")
add_output(f"XБ_opt = ({base[0], base[1]})")
add_output(f"A_i = {conjugate_result['A_i']}")
add_output(f"C_i = {conjugate_result['C_i']}")
add_output("AT_i * Y = C_i")
add_output("Решаем систему")
add_output("{" + f"{row_to_equation(conjugate_result['A_i'][0], var='y')} = {conjugate_result['C_i'][0]}")
add_output("{" + f"{row_to_equation(conjugate_result['A_i'][1], var='y')} = {conjugate_result['C_i'][1]}")
add_output("Ответ:")
add_output("{" + f"y1 = {conjugate_result['y1']}")
add_output("{" + f"y2 = {conjugate_result['y2']}")
add_output("Проверим целевую функцию:")
eq = row_to_equation(reversed_canonical['C'], var='y')
y1,y2 = symbols('y1 y2')
add_output(f"F = {eq} = {sympify(eq).subs({y1: conjugate_result['y1'], y2: conjugate_result['y2']})}")