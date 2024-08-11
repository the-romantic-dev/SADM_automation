from pathlib import Path

from report.model.elements.formula import Formula
from report.model.elements.paragraph import Paragraph
from report.model.elements.plain_text import PlainText
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import elements_list, formula
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.view.solution_tf import SolutionTF
from tasks.task1_2_lp.view.symplex.table_symplex_solution.symplex_table import SymplexTable
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel

template_path = Path(Path(__file__).parent, "table_symplex_solution.docx")


class TableSymplexSolutionTF(SolutionTF):
    def __init__(self, solutions: list[BasisSolution], swaps: list[tuple[int, int]],
                 start_basis_index: int):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.solutions = solutions
        self.swaps = swaps
        self.start_basis_index = start_basis_index

    @elements_list
    def _fill_solution_steps(self):
        _elements_list = []
        for i, sol in enumerate(self.solutions):
            swap = self.swaps[i] if i < len(self.swaps) else None
            symplex_table = SymplexTable(sol, swap)
            basis_variables_latex = BasisSolutionViewModel(sol).basis_variables_latex
            current_index = self.start_basis_index + i
            paragraph_data = [
                PlainText(text=f"Базис {current_index}: ", bold=True, italic=False, size=28),
                Formula(",".join(basis_variables_latex), font_size=28, bold=True)
            ]
            _elements_list.append(Paragraph(paragraph_data))
            _elements_list.append(symplex_table.table)
        return _elements_list

    @formula
    def _fill_result(self):
        return self.result_formula(self.solutions[-1])
