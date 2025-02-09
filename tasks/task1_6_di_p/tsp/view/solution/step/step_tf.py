from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, formula, elements_list, table, image
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportData
from tasks.task1_6_di_p.tsp.view.solution.graph_builder import build_graph
from tasks.task1_6_di_p.tsp.view.solution.util import get_previous_G_latex, get_exclude_G_latex, get_include_G_latex, \
    matrix_to_table

dir = Path(__file__).parent
template_path = Path(dir, "step.docx")


@sub_tf
class StepTF(TemplateFiller):
    def __init__(self, solution_data: list, step: int):
        self.solution_data = solution_data
        self.step_data: TSPReportData = solution_data[step]
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

    @elements_list
    def _fill_taus(self):
        elements = []
        for tau in self.step_data.taus:
            formula_data = [
                f"\\tau\\left( {tau[0][0] + 1},{tau[0][1] + 1} \\right) = ",
                f"{tau[2][0]} + {tau[2][1]} = {tau[1]} "
            ]
            elements.append(Formula(formula_data))
        return elements

    @formula
    def _fill_exclude_G(self):
        return Formula(get_exclude_G_latex(self.step_data))

    @formula
    def _fill_u(self):
        u = self.step_data.worst_tau
        return Formula(f"u\\left( {u[0][0] + 1},{u[0][1] + 1} \\right) = {u[1]}")

    @formula
    def _fill_exclude_v(self):
        worst_tau = self.step_data.worst_tau
        previous_v = self.step_data.previous_evaluation
        exclude_v = self.step_data.exclude_evaluation
        formula_data = [
            f"V({get_exclude_G_latex(self.step_data)}) =",
            f"V({get_previous_G_latex(self.step_data)}) + u({worst_tau[0][0] + 1},{worst_tau[0][1] + 1}) = ",
            f"{previous_v} + {worst_tau[1]} = {exclude_v}"
        ]

        return Formula(formula_data)

    @table
    def _fill_table_removed_kl(self):
        return matrix_to_table(self.step_data.trimmed_matrix.matrix)

    @table
    def _fill_table_filtered_paths(self):
        return matrix_to_table(self.step_data.filtered_paths_matrix.matrix)

    @table
    def _fill_table_zeroing(self):
        return matrix_to_table(self.step_data.zeroing_matrix.matrix)

    @formula
    def _fill_h(self):
        formula_data = [
            f"h = {sum(self.step_data.h_terms)}"
        ]
        return Formula(formula_data)

    @formula
    def _fill_include_G(self):
        return Formula(get_include_G_latex(self.step_data))

    @formula
    def _fill_include_v(self):
        terms = self.step_data.h_terms
        h = sum(terms)
        previous_evaluation = self.step_data.previous_evaluation
        include_evaluation = self.step_data.include_evaluation
        formula_data = [
            f"V({get_include_G_latex(self.step_data)}) =",
            f"V({get_previous_G_latex(self.step_data)}) +  h =",
            f" {previous_evaluation} + {h} = {include_evaluation}"
        ]

        return Formula(formula_data)

    @formula
    def _fill_result_eq(self):
        is_next_from_candidates = self.step_data.is_next_from_candidates
        if not is_next_from_candidates:
            is_included = self.step_data.is_included
            if is_included:
                formula_data = [
                    f"V({get_include_G_latex(self.step_data)}) < ",
                    f"V({get_exclude_G_latex(self.step_data)})"
                ]
            else:
                formula_data = [
                    f"V({get_exclude_G_latex(self.step_data)}) < ",
                    f"V({get_include_G_latex(self.step_data)})"
                ]
        else:
            return None
        return Formula(formula_data)

    @text
    def _fill_result_txt(self):
        is_next_from_candidates = self.step_data.is_next_from_candidates
        if not is_next_from_candidates:
            is_included = self.step_data.is_included
            if is_included:
                txt = " значит дальше идем по ветке, включающей вершину"
            else:
                txt = (" значит дальше идем по ветке, исключающей вершину, кроме того преобразуем матрицу, как "
                       "указано в теории")
        else:
            txt = ("В одной из висячих вершин оценочная функция V меньше чем любая на этом шаге. "
                   "Значит переходим к ней")
        return txt

    @image
    def _fill_graph(self):
        dot = build_graph(self.solution_data[:self.step + 1])
        img_path = Path(dir, 'graph.png')
        dot.render(Path(dir, 'graph'))
        return img_path
