from pathlib import Path

from report.model.elements.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, elements_list
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel

template_path = Path(Path(__file__).parent, "problem.docx")


@sub_tf
class ProblemTF(TemplateFiller):
    def __init__(self, variant: int, lpp_vm: LPProblemViewModel):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.variant = variant
        self.lpp_vm = lpp_vm

    @text
    def _fill_variant(self):
        return str(self.variant)

    @elements_list
    def _fill_problem(self):
        return [Formula(ltx) for ltx in self.lpp_vm.problem_latex()]
