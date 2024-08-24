from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import elements_list
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel

template_path = Path(Path(__file__).parent, "canonical_problem.docx")


@sub_tf
class CanonicalProblemTF(TemplateFiller):
    def __init__(self, lpp_vm: LPProblemViewModel):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.lpp_vm = lpp_vm

    @elements_list
    def _fill_canonical_problem(self):
        return [Formula(ltx) for ltx in self.lpp_vm.canonical_problem_latex()]
