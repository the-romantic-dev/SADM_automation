from sympy import Float, pretty

from report.docx.pretty_omml import sympy_matrix_to_omml
from report.model.document_template import DocumentTemplate
from report.model.filler_decorators import formula
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller
from tasks.task1_2_lp.document_template.matrix_symplex.util import elements as ms_elements, \
    formula_data as ms_formula_data
from tasks.task1_2_lp.document_template.matrix_symplex.util.step_data import MatrixSymplexStepData
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


class OptPartTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, step_data: MatrixSymplexStepData):
        super().__init__(template)
        self.step_data = step_data

    @formula
    def _fill_basis_value(self):
        element = ms_elements.basis_value(self.step_data.current_index)
        return Formula(element)

    @formula
    def _fill_basis_value_expression(self):
        data = ms_formula_data.basis_value_expression(self.step_data)
        return Formula(data)

    @formula
    def _fill_F_expression(self):
        data = ms_formula_data.F_expression(self.step_data)
        return Formula(data)
