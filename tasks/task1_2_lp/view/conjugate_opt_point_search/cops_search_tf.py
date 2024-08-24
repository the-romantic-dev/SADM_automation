from pathlib import Path

from sympy import latex, Matrix

from report.docx.omml import latex2omml
from report.model.elements.math.matrix import sympy_matrix_to_omml
from report.model.elements.math.braces import braces
from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model import BasisSolution

template_path = Path(Path(__file__).parent, "conjugate_opt_point_search.docx")


class COPSSearchTF(TemplateFiller):
    def __init__(self, opt_sol: BasisSolution):
        self.opt_sol = opt_sol
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @formula
    def _fill_X_opt(self):
        X_latex = "X_{opt}^{Б}"
        variables = self.opt_sol.basis_variables
        variables_element = latex2omml(",".join([latex(v) for v in variables]))
        formula_data = [
            f"{X_latex} = ",
            braces(variables_element)
        ]
        return Formula(formula_data)

    @formula
    def _fill_A_i(self):
        A = self.opt_sol.lp_problem.canonical_form.matrices[0]
        basis = self.opt_sol.basis
        A_i = Matrix.hstack(A.col(basis[0]), A.col(basis[1]))
        formula_data = [
            f"A_i = ",
            sympy_matrix_to_omml(A_i)
        ]
        return Formula(formula_data)

    @formula
    def _fill_C_i(self):
        C = self.opt_sol.lp_problem.canonical_form.matrices[2]
        basis = self.opt_sol.basis
        C_i = Matrix([C[basis[0], 0], C[basis[1], 0]])
        formula_data = [
            f"C_i = ",
            sympy_matrix_to_omml(C_i)
        ]
        return Formula(formula_data)
