from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, formula, table, image
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportDataLast
from tasks.task1_6_di_p.tsp.view.solution.graph_builder import build_graph
from tasks.task1_6_di_p.tsp.view.solution.util import get_previous_G_latex, matrix_to_table

template_path = Path(Path(__file__).parent, "last_step.docx")
dir = Path(__file__).parent

@sub_tf
class LastStepTF(TemplateFiller):
    def __init__(self, solution_data: list, step: int):
        self.solution_data = solution_data
        self.step_data: TSPReportDataLast = solution_data[step]
        self.step = step
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @text
    def _fill_step_number(self):
        return str(self.step)

    @formula
    def _fill_current_G(self):
        return Formula(get_previous_G_latex(self.step_data))

    @table
    def _fill_start_table(self):
        return matrix_to_table(self.step_data.start_matrix.matrix)

    @formula
    def _fill_result_path(self):
        result_path = self.step_data.result_path

        graph = {}
        for edge in result_path:
            if edge[0] not in graph:
                graph[edge[0]] = edge[1]

        def dfs(node, _visited, segment):
            segment.append(node)
            if node in graph and not _visited.get(node, False):
                _visited[node] = True
                dfs(node=graph[node], _visited=_visited, segment=segment)

        visited = {node: False for node in graph}
        result = []
        dfs(node=result_path[0][0], _visited=visited, segment=result)
        return Formula('\\rightarrow '.join([str(i + 1) for i in result]))

    @image
    def _fill_graph(self):
        dot = build_graph(self.solution_data)
        img_path = Path(dir, 'graph.png')
        dot.render(Path(dir, 'graph'))
        return img_path
