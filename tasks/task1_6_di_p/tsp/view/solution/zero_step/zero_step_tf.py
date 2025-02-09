from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, table
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportDataMinimal
from tasks.task1_6_di_p.tsp.view.solution.util import matrix_to_table

template_path = Path(Path(__file__).parent, "zero_step.docx")


@sub_tf
class ZeroStepTF(TemplateFiller):
    def __init__(self, step_data: TSPReportDataMinimal):
        self.step_data = step_data
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @table
    def _fill_table_zeroing(self):
        return matrix_to_table(self.step_data.zeroing_matrix.matrix)

    @formula
    def _fill_h(self):
        formula_data = [
            f"h = {sum(self.step_data.h_terms)}"
        ]
        return Formula(formula_data)
