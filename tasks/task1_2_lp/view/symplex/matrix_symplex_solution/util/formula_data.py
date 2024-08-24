from sympy import sign

import tasks.task1_2_lp.view.symplex.matrix_symplex_solution.util.latex as ms_latex
import tasks.task1_2_lp.view.symplex.matrix_symplex_solution.util.matrices as ms_matrices
import tasks.task1_2_lp.view.symplex.matrix_symplex_solution.util.elements as ms_elements
from report.model.elements.pretty_elements import sympy_matrix_to_omml
from report.model.report_prettifier import rational_latex
from tasks.task1_2_lp.view.symplex.step_data import SymplexStepData


def CTB_equation(step_data):
    return [
        f"{ms_latex.CTB(step_data.current_index)} = ",
        sympy_matrix_to_omml(ms_matrices.CTB(step_data.current_solution))
    ]


def P_equation(step_data: SymplexStepData):
    return [
        f"{ms_latex.P(step_data.current_index)} = ",
        sympy_matrix_to_omml(ms_matrices.P(step_data.current_solution))
    ]


def P_inv_equation(step_data: SymplexStepData):
    return [
        f"{ms_latex.P_inv(step_data.current_index)} = ",
        sympy_matrix_to_omml(ms_matrices.P_inv(step_data.current_solution))
    ]


def delta_equation(step_data: SymplexStepData, free_var_index: int):
    ctb_vector = ms_matrices.CTB(step_data.current_solution)
    p_matrix = ms_matrices.P(step_data.current_solution)
    a_column = ms_matrices.A_column(step_data.current_solution, free_var_index)
    c_elem = ms_matrices.C_element(step_data.current_solution, free_var_index)
    result = (ctb_vector * p_matrix * a_column)[0, 0] - c_elem

    c_sign = "-" if c_elem >= 0 else " + "

    formula_data = [
        f"{ms_latex.delta(free_var_index)} = ",
        ms_latex.CTB(step_data.current_index),
        ms_latex.P_inv(step_data.current_index),
        f"{ms_latex.A_column(free_var_index)} - ",
        f"{ms_latex.C_element(free_var_index)} = ",
        sympy_matrix_to_omml(ctb_vector),
        sympy_matrix_to_omml(p_matrix),
        sympy_matrix_to_omml(a_column),
        f" {c_sign} {c_elem * sign(c_elem)} = ",
        f"{rational_latex(result)}"
    ]
    return formula_data


def basis_value_expression(step_data: SymplexStepData):
    P_inv = ms_matrices.P_inv(step_data.current_solution)
    b = ms_matrices.b(step_data.current_solution)
    result = P_inv * b
    formula_data = [
        ms_elements.basis_value(step_data.current_index),
        f" = {ms_latex.P_inv(step_data.current_index)}b = ",
        sympy_matrix_to_omml(P_inv),
        sympy_matrix_to_omml(b),
        " = ",
        sympy_matrix_to_omml(result)
    ]
    return formula_data


def Z_column_expression(step_data: SymplexStepData):
    P_inv = ms_matrices.P_inv(step_data.current_solution)
    A = ms_matrices.A_column(step_data.current_solution, step_data.in_var)
    result = ms_matrices.Z(step_data.current_solution, step_data.in_var)
    data = [
        f"{ms_latex.Z(step_data.in_var)} = ",
        ms_latex.P_inv(step_data.current_index),
        f"{ms_latex.A_column(step_data.in_var)} = ",
        sympy_matrix_to_omml(P_inv),
        sympy_matrix_to_omml(A),
        " = ",
        sympy_matrix_to_omml(result)

    ]
    return data


def basis_exclude_criteria_expression(step_data: SymplexStepData):
    result = []
    basis = step_data.current_solution.basis
    Z = ms_matrices.Z(step_data.current_solution, step_data.in_var)

    for i, b in enumerate(basis):
        basis_element_value = step_data.current_solution.basis_values[i]
        z_element_value = Z[i, 0]
        z_index = f"{i + 1}{step_data.in_var + 1}"
        if z_element_value > 0:
            data = [
                ms_elements.basis_exclude_criteria_frac(
                    basis_index=step_data.current_index,
                    element_index=b + 1,
                    z_index=z_index
                ),
                f" = \\frac{{{rational_latex(basis_element_value)}}}{{{rational_latex(z_element_value)}}} =",
                f"{rational_latex(basis_element_value / z_element_value)}"
            ]
        else:
            data = [f"z_{{{z_index}}} \\le 0"]
        result.append(data)
    return result


def F_expression(step_data: SymplexStepData):
    ctb = ms_matrices.CTB(step_data.current_solution)
    P = ms_matrices.P(step_data.current_solution)
    b = ms_matrices.b(step_data.current_solution)
    result = (ctb * P * b)[0, 0]
    decimal = result.evalf()
    string = f"{decimal:.15f}".rstrip('0').rstrip('.')
    formula_data = [
        "F = ",
        ms_latex.CTB(step_data.current_index),
        ms_latex.P_inv(step_data.current_index),
        "b = ",
        sympy_matrix_to_omml(ctb),
        sympy_matrix_to_omml(P),
        sympy_matrix_to_omml(b),
        f" = {string}"
    ]
    return formula_data
