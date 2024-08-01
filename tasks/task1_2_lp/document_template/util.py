from pathlib import Path

from sympy import latex, Eq, Expr, Matrix

from report.docx.docx_namespaces import m, w
from report.docx.pretty_omml import replace_in_xml, element_from_string_with_namespaces, sympy_matrix_to_omml
from report.model.formula import Formula
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


def eq_latex(left: Expr, right: Expr):
    return latex(Eq(left, right))
