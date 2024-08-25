from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import template_filler
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import root_tf
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.model.util import start_X
from tasks.task1_3_nlp_unlimited.view.analitical_solution.nlpu_analitical_solution_tf import NLPUAnalyticalSolutionTF
from tasks.task1_3_nlp_unlimited.view.common_iterations.nlpu_common_iterations_tf import NLPUCommonIterationsTF
from tasks.task1_3_nlp_unlimited.view.problem.nlpu_problem_tf import NLPUProblemTF
from tasks.teacher import Teacher

sabonis_template_path = Path(Path(__file__).parent, "nlp_unlimited_main.docx")
sidnev_template_path = None


@root_tf
class NLPUnlimitedMainTF(TemplateFiller):
    def __init__(self, teacher: Teacher, variant: int, objective: NLPObjective, nickname: str):
        # self.nickname = nickname
        self.objective = objective
        self.variant = variant
        self.teacher = teacher

        self.start_X = start_X(objective, nickname)
        curr_path = sabonis_template_path

        if teacher == Teacher.SIDNEV:
            curr_path = sidnev_template_path
        template = DocumentTemplate(curr_path)
        super().__init__(template)

    @template_filler
    def _fill_problem(self):
        return NLPUProblemTF(teacher=self.teacher, objective=self.objective, variant=self.variant)

    @template_filler
    def _fill_analytical_solution(self):
        return NLPUAnalyticalSolutionTF(self.objective)

    @template_filler
    def _fill_common_iterations_part(self):
        return NLPUCommonIterationsTF(self.objective, self.start_X)
