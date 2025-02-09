from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.docx_parts.table import Table
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import table, elements_list, text
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import root_tf
from tasks.task1_6_di_p.tsp.view.solution.last_step.last_step_tf import LastStepTF
from tasks.task1_6_di_p.tsp.view.solution.step.step_tf import StepTF
from tasks.task1_6_di_p.tsp.view.solution.zero_step.zero_step_tf import ZeroStepTF

template_path = Path(Path(__file__).parent, "main.docx")


@root_tf
class MainTF(TemplateFiller):
    def __init__(self, variant: int, task_table: list[list], solution_data: list):
        self.task_table = task_table
        self.variant = variant
        self.solution_data = solution_data
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @text
    def _fill_variant(self):
        return str(self.variant)

    @table
    def _fill_task_table(self):
        table_data = [
            [Formula(str(elem)) for elem in row]
            for row in self.task_table
        ]

        return Table(
            table_data=table_data,
            color_fills=dict()
        )

    @elements_list
    def _fill_solution(self):
        filled_documents = []
        for step, step_data in enumerate(self.solution_data):
            if step == 0:
                tf = ZeroStepTF(step_data)
            elif step == len(self.solution_data) - 1:
                tf = LastStepTF(solution_data=self.solution_data, step=step)
            else:
                tf = StepTF(solution_data=self.solution_data, step=step)
            tf.fill()
            filled_documents.append(tf.template.document)
            # in_var = None
            # out_var = None
            # if i < len(self.swaps):
            #     swap = self.swaps[i]
            #     in_var = swap[1]
            #     out_var = swap[0]
            # current_index = self.start_basis_index + i
            # step_data = SymplexStepData(current_solution=sol, current_index=current_index, in_var=in_var,
            #                             out_var=out_var)
            # matrix_symplex_step_tf = MatrixSymplexStepTF(step_data)
            # matrix_symplex_step_tf.fill()
            #
            # filled_documents.append(matrix_symplex_step_tf.template.document)
        return filled_documents