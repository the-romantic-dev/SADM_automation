from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util import elements as ms_elements
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util import formula_data as ms_formula_data
from tasks.task1_2_lp.view.template_fillers.symplex.util.step_data import SymplexStepData


class OptPartTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, step_data: SymplexStepData):
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
