from pathlib import Path

from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.viewmodel.nlp_objective_vm import nlp_objective_element
from tasks.teacher import Teacher

sabonis_template_path = Path(Path(__file__).parent, "sabonis_nlpu_problem.docx")
sidnev_template_path = Path()


class NLPUProblemTF(TemplateFiller):
    def __init__(self, teacher: Teacher, objective: NLPObjective, variant: int):
        self.variant = variant
        self.objective = objective
        self.teacher = teacher

        curr_path = sabonis_template_path
        if teacher == Teacher.SIDNEV:
            curr_path = sidnev_template_path
        template = DocumentTemplate(curr_path)
        super().__init__(template)

    @text
    def _fill_variant(self):
        return str(self.variant)

    @formula
    def _fill_objective(self):
        formula_data = [
            'max',
            nlp_objective_element(self.objective)
        ]
        return Formula(formula_data)
