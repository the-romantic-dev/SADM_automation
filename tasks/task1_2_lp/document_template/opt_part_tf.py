from sympy import Float, pretty

from report.docx.pretty_omml import sympy_matrix_to_omml, replace_rationals_expr
from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller
from tasks.task1_2_lp.document_template.util import P_matrix, CTB_latex, CTB_vector, basis_value_element, P_inv_latex, \
    b_vector
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


class OptPartTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, basis_solution: BasisSolution, solution_index: int):
        super().__init__(template)
        self.solution_index = solution_index
        self.basis_solution = basis_solution

    @TemplateFiller.filler_method
    def _fill_basis_value(self):
        element = basis_value_element(self.solution_index)
        formula = Formula(element)
        self.template.insert_formula(key="basis_value", formula=formula)

    @TemplateFiller.filler_method
    def _fill_basis_value_expression(self):
        P = P_matrix(self.basis_solution).inv()
        b = b_vector(self.basis_solution)
        result = P * b
        formula_data = [
            basis_value_element(self.solution_index),
            f" = {P_inv_latex(self.solution_index)}b = ",
            sympy_matrix_to_omml(P),
            sympy_matrix_to_omml(b),
            " = ",
            sympy_matrix_to_omml(result)
        ]
        formula = Formula(formula_data)
        self.template.insert_formula(key="basis_value_expression", formula=formula)

    @TemplateFiller.filler_method
    def _fill_F_expression(self):
        ctb = CTB_vector(self.basis_solution)
        P = P_matrix(self.basis_solution)
        b = b_vector(self.basis_solution)
        result = (ctb * P * b)[0, 0]
        decimal = result.evalf()
        string = f"{decimal:.15f}".rstrip('0').rstrip('.')
        formula_data = [
            "F = ",
            CTB_latex(self.solution_index),
            P_inv_latex(self.solution_index),
            "b = ",
            sympy_matrix_to_omml(ctb),
            sympy_matrix_to_omml(P),
            sympy_matrix_to_omml(b),
            f" = {string}"
        ]
        formula = Formula(formula_data)
        self.template.insert_formula(key="F_expression", formula=formula)