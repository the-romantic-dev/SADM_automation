from pathlib import Path

from sympy import latex, Eq, Expr, Matrix

from report.docx.docx_namespaces import m, w
from report.docx.pretty_omml import replace_in_xml, element_from_string_with_namespaces
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


def eq_latex(left: Expr, right: Expr):
    return latex(Eq(left, right))


def CTB_latex(index: int):
    return f"C^{{TБ_{index}}}"


def CTB_vector(basis_solution: BasisSolution):
    coeffs = basis_solution.lp_problem.canonical_form.matrices[-1]
    vector = Matrix([coeffs[i] for i in basis_solution.basis]).T
    return vector


def P_latex(index: int):
    return f"P_{index}"


def P_matrix(basis_solution: BasisSolution):
    A = basis_solution.lp_problem.canonical_form.matrices[0]
    basis = list(basis_solution.basis)
    return Matrix(A[:, basis])


def basis_value_element(basis_index: int):
    TEMPLATES_DIR = Path(TASK_DIR, "templates/sabonis/matrix_symplex/")
    txt_path = Path(TEMPLATES_DIR, "basis_value.txt")
    with open(txt_path.as_posix(), 'r', encoding='utf-8') as file:
        formula_xml = file.read()
    replaced_xml = replace_in_xml(formula_xml, key="basis_index", data=str(basis_index))
    element = element_from_string_with_namespaces(replaced_xml, {"m": m, "w": w})[0]
    return element


def b_vector(basis_solution: BasisSolution):
    return basis_solution.lp_problem.matrices[1]


def P_inv_latex(index: int):
    return f"P_{index}^{{-1}}"
