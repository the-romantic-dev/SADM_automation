from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import elements_list
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel
from tasks.teacher import Teacher

template_path = Path(Path(__file__).parent, "dual_problem.docx")


@sub_tf
class DualProblemTF(TemplateFiller):
    def __init__(self, lpp: LPProblem):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.lppvm = LPProblemViewModel(lpp)

    @elements_list
    def _fill_problem(self):
        return [Formula(data) for data in self.lppvm.canonical_problem_latex()]

    @elements_list
    def _fill_dual_problem(self):
        return [Formula(data) for data in self.lppvm.dual_problem_latex(from_canonical=True)]
