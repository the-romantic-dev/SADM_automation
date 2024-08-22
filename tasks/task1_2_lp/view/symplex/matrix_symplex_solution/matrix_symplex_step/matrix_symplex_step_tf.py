import os
from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, formula, elements_list, document
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.non_opt_part.non_opt_part_tf import NonOptPartTF
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.opt_part.opt_part_tf import OptPartTF
from tasks.task1_2_lp.view.symplex.step_data import SymplexStepData
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.util import latex as ms_latex
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.util import formula_data as ms_fd

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "matrix_symplex_step.docx")


@sub_tf
class MatrixSymplexStepTF(TemplateFiller):
    def __init__(self, step_data: SymplexStepData):
        template = DocumentTemplate(template_path)
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
        step_data = self.step_data
        if step_data.current_solution.is_opt:
            tf = OptPartTF(step_data)
        else:
            tf = NonOptPartTF(step_data)
        tf.fill()
        return tf.template.document
