from docx import Document
from docx.document import Document as DocumentType

from report.docx.pretty_omml import braces, elements_list_to_matrix_element, BraceType
from report.model.elements.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel


class AuxiliaryTaskTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, lp_problem: LPProblem):
        super().__init__(template)
        self.lp_problem = lp_problem
        self.lp_problem_vm = LPProblemViewModel(lp_problem)

    @formula
    def _fill_canonical_artificial_transformation(self):
        canonical_latex = self.lp_problem_vm.canonical_problem_latex()
        canonical_formulas = [Formula(l) for l in canonical_latex]
        canonical_omml = [f.oMath for f in canonical_formulas]
        canonical_problem_as_matrix = elements_list_to_matrix_element([[e] for e in canonical_omml], alignment="left")
        canonical_brace = braces(canonical_problem_as_matrix, BraceType.LEFT_CURLY)
        formula_data = [canonical_brace, "\\rightarrow"]
        return Formula(formula_data)
