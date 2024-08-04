from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, elements_list
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.view.template_fillers.symplex.util.step_data import SymplexStepData
import tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util.latex as ms_latex
import tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util.formula_data as ms_formula_data
import tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util.elements as ms_elements


class NonOptPartTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, step_data: SymplexStepData):
        super().__init__(template)
        self.step_data = step_data

    @formula
    def _fill_min_delta_expression(self):
        data = ms_latex.min_delta_expression(self.step_data.in_var)
        return Formula(data)

    @formula
    def _fill_basis_in_variable(self):
        return Formula(f"x_{self.step_data.in_var + 1}")

    @formula
    def _fill_Z_column(self):
        return Formula(ms_latex.Z(self.step_data.in_var))

    @formula
    def _fill_Z_column_expression(self):
        data = ms_formula_data.Z_column_expression(self.step_data)
        return Formula(data)

    @formula
    def _fill_basis_value(self):
        element = ms_elements.basis_value(self.step_data.current_index)
        return Formula(element)

    @formula
    def _fill_basis_value_expression(self):
        data = ms_formula_data.basis_value_expression(self.step_data)
        return Formula(data)

    @formula
    def _fill_basis_exclude_criteria(self):
        element = ms_elements.basis_exclude_criteria(self.step_data.current_index)
        return Formula(element)

    @elements_list
    def _fill_basis_exclude_criteria_expression(self):
        data_list = ms_formula_data.basis_exclude_criteria_expression(self.step_data)
        return [Formula(data) for data in data_list]


    @formula
    def _fill_basis_out_variable(self):
        return Formula(f"x_{self.step_data.out_var + 1}")

