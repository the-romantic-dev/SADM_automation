from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, formula, elements_list, document
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.view.template_fillers.symplex.util.step_data import SymplexStepData
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util import template_fillers as ms_tf
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.util import latex as ms_latex, formula_data as ms_fd


class MatrixSymplexStepTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, step_data: SymplexStepData):
        super().__init__(template)
        self.step_data = step_data

    @text
    def _fill_index(self):
        return str(self.step_data.current_index)

    @formula
    def _fill_basis_variables(self):
        data = ms_latex.basis_variables(self.step_data.current_solution)
        return Formula(data, font_size=28, bold=True)

    @formula
    def _fill_P_matrix(self):
        data = ms_latex.P(self.step_data.current_index)
        return Formula(data)

    @formula
    def _fill_P_matrix_equation(self):
        data = ms_fd.P_equation(self.step_data)
        return Formula(data)

    @formula
    def _fill_P_inverse_matrix(self):
        data = ms_latex.P_inv(self.step_data.current_index)
        return Formula(data)

    @formula
    def _fill_P_inverse_matrix_equation(self):
        data = ms_fd.P_inv_equation(self.step_data)
        return Formula(data)

    @formula
    def _fill_CTB_vector(self):
        data = ms_latex.CTB(self.step_data.current_index)
        return Formula(data)

    @formula
    def _fill_CTB_vector_equation(self):
        data = ms_fd.CTB_equation(self.step_data)
        return Formula(data)

    @elements_list
    def _fill_deltas_equations(self):
        data_producer = ms_fd.delta_equation
        free = self.step_data.current_solution.free
        return [Formula(data_producer(self.step_data, var_i)) for var_i in free]

    @document
    def _fill_opt_dependency_part(self):
        tf = ms_tf.opt_tf(self.step_data)
        tf.fill()
        return tf.template.document
