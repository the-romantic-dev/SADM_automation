import os
from pathlib import Path

from report.model.elements.math.matrix import elements_list_to_matrix_element
from report.model.elements.math.braces import BraceType, braces
from report.model.docx_parts.formula import Formula
from report.model.docx_parts.paragraph import Paragraph
from report.model.docx_parts.plain_text import PlainText
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, elements_list
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model import BasisSolution
from tasks.task1_2_lp.view.symplex.table_symplex_solution.symplex_table import SymplexTable
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel


def problem_element(problem_latex: list[str]):
    problem_formulas = [Formula(l) for l in problem_latex]
    problem_omml = [f.oMath for f in problem_formulas]
    problem_problem_as_matrix = elements_list_to_matrix_element([[e] for e in problem_omml], alignment="left")
    result = braces(problem_problem_as_matrix, BraceType.LEFT_CURLY)
    return result


package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "auxiliary_task.docx")


@sub_tf
class AuxiliaryTaskTF(TemplateFiller):
    def __init__(self, lpp_vm: LPProblemViewModel, auxiliary_solution: list[BasisSolution],
                 auxiliary_swaps: list[tuple[int, int] | None]):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.lpp_vm = lpp_vm
        self.sol = auxiliary_solution
        self.swaps = auxiliary_swaps

    @formula
    def _fill_canonical_artificial_transformation(self):
        canonical_brace = problem_element(self.lpp_vm.canonical_problem_latex())
        art_form_brace = problem_element(self.lpp_vm.art_form_latex())
        formula_data = [canonical_brace, "\\rightarrow", art_form_brace]
        return Formula(formula_data)

    @formula
    def _fill_auxiliary_problem(self):
        formula_data = problem_element(self.lpp_vm.auxiliary_form_latex())
        return Formula(formula_data)

    @elements_list
    def _fill_start_basis_symplex_search(self):
        self.swaps.append(None)
        _elements_list = []
        for i, sol, swap in zip(range(len(self.sol)), self.sol, self.swaps):
            basis_variables_latex = BasisSolutionViewModel(sol).basis_variables_latex
            symplex_table = SymplexTable(sol, swap)
            paragraph_data = [
                PlainText(text=f"Базис {i}: ", bold=True, italic=False, size=28),
                Formula(",".join(basis_variables_latex), font_size=28, bold=True)
            ]
            _elements_list.append(Paragraph(paragraph_data))
            _elements_list.append(symplex_table.symplex_table)
        return _elements_list

    @formula
    def _fill_acceptable_basis(self):
        basis_latex = BasisSolutionViewModel(self.sol[-1]).basis_variables_latex
        return Formula(",".join(basis_latex))
