import hashlib
import random
from pathlib import Path

from sympy import Matrix, Rational

from report.model.docx_parts.formula import Formula
from report.model.elements.math.matrix import matrix_from_sympy
from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective

template_path = Path(Path(__file__).parent, "common_iterations.docx")

@sub_tf
class CommonIterationsTF(TemplateFiller):
    def __init__(self, objective: NLPObjective, start_X: tuple[Rational, Rational]):
        self.objective = objective
        self.start_X = start_X
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @formula
    def _fill_start_X(self):
        formula_data = [
            "X^{(0)} = ",
            matrix_from_sympy(Matrix(list(self.start_X)))
        ]
        return Formula(formula_data)

    @formula
    def _fill_start_objective_value(self):
        value = self.objective.value(Matrix(list(self.start_X)))
        formula_data = [
            "f(X^{(0)}) = ",
            rational_latex(value)
        ]
        return Formula(formula_data)