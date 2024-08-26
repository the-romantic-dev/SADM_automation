from pathlib import Path

from sympy import Matrix

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import template_filler
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import root_tf
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.model.util import start_X
from tasks.task1_3_nlp_unlimited.view.analitical_solution.analytical_solution_tf import AnalyticalSolutionTF
from tasks.task1_3_nlp_unlimited.view.common_iterations.common_iterations_tf import CommonIterationsTF
from tasks.task1_3_nlp_unlimited.view.methods.rapid_ascent_method.rapid_ascent_method_tf import RapidAscentMethodTF
from tasks.task1_3_nlp_unlimited.view.methods.relaxation_method.relaxation_method_tf import RelaxationMethodTF
from tasks.task1_3_nlp_unlimited.view.problem.problem_tf import ProblemTF
from tasks.teacher import Teacher

sabonis_template_path = Path(Path(__file__).parent, "sabonis_main.docx")
sidnev_template_path = Path(Path(__file__).parent, "sidnev_main.docx")


@root_tf
class MainTF(TemplateFiller):
    def __init__(self, teacher: Teacher, variant: int, objective: NLPObjective, nickname: str):
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
        return ProblemTF(teacher=self.teacher, objective=self.objective, variant=self.variant)

    @template_filler
    def _fill_analytical_solution(self):
        return AnalyticalSolutionTF(self.objective)

    @template_filler
    def _fill_common_iterations_part(self):
        return CommonIterationsTF(self.objective, self.start_X)

    @template_filler
    def _fill_relaxation_method(self):
        return RelaxationMethodTF(self.objective, Matrix(self.start_X), self.teacher)

    @template_filler
    def _fill_rapid_ascent_method(self):
        return RapidAscentMethodTF(self.objective, Matrix(self.start_X), self.teacher)
