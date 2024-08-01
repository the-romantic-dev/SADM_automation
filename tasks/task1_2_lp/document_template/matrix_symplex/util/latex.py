from sympy import latex

from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


def basis_variables(current_solution: BasisSolution) -> str:
    result = ",".join([latex(variable) for variable in current_solution.basis_variables])
    return result


def P(current_index: int) -> str: return f"P_{current_index}"


def P_inv(current_index: int) -> str: return f"{P(current_index)}^{{-1}}"


def CTB(current_index: int) -> str: return f"C^{{TБ_{current_index}}}"


def A_column(var_index: int) -> str: return f"A_{var_index + 1}"


def C_element(var_index: int) -> str: return f"c_{var_index + 1}"


def delta(var_index: int) -> str: return f"\\Delta_{var_index + 1}"


def min_delta_expression(in_var: int) -> str: return f"{delta(in_var)} = min(\\Delta_j)"


def Z(var_index: int): return f"Z_{var_index + 1}"
