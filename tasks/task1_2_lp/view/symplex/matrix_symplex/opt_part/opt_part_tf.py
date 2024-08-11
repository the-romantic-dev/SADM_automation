import os
from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.view.symplex.matrix_symplex.util import elements as ms_elements, formula_data as ms_formula_data
from tasks.task1_2_lp.view.symplex.step_data import SymplexStepData

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "opt_part.docx")


class OptPartTF(TemplateFiller):
    def __init__(self, step_data: SymplexStepData):
        template = DocumentTemplate(template_path)
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
