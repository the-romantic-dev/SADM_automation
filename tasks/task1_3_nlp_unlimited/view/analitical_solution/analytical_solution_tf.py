from pathlib import Path

from sympy import latex, Matrix, Eq, solve

from report.docx.omml import latex2omml
from report.model.docx_parts.formula import Formula
from report.model.elements.math.braces import BraceType
from report.model.elements.math.matrix import matrix_from_elements, matrix_from_sympy
from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.model.util import solution_matrix

template_path = Path(Path(__file__).parent, "analytical_solution.docx")


@sub_tf
class AnalyticalSolutionTF(TemplateFiller):
    def __init__(self, objective: NLPObjective):
        self.objective = objective
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @formula
    def _fill_gradient_objective(self):
        gradient = self.objective.grad()
        grad_elements = [latex2omml(latex(g)) for g in gradient]
        formula_data = [
            r"\nabla f(X) = ",
            matrix_from_elements([[grad_elements[0]], [grad_elements[1]]], alignment='center',
                                 brace_type=BraceType.PARENTHESES),
        ]
        return Formula(formula_data)

    @formula
    def _fill_gradient_zero_equation_system(self):
        gradient = self.objective.grad()
        grad_elements = [latex2omml(f"{latex(g)} = 0") for g in gradient]
        formula_data = [
            matrix_from_elements([[grad_elements[0]], [grad_elements[1]]], alignment='right',
                                 brace_type=BraceType.LEFT_CURLY),
        ]
        return Formula(formula_data)

    @formula
    def _fill_opt_X(self):
        formula_data = [
            "X^* = ",
            matrix_from_sympy(solution_matrix(self.objective))
        ]
        return Formula(formula_data)

    @formula
    def _fill_gesse_matrix(self):
        gesse = self.objective.gesse()
        formula_data = [
            "H(X^*) = ",
            matrix_from_sympy(Matrix(gesse))
        ]
        return Formula(formula_data)

    @formula
    def _fill_quadratic_form(self):
        sol = solution_matrix(self.objective)
        H = Matrix(self.objective.gesse())
        formula_data = [
            matrix_from_sympy(sol.T),
            "\\cdot",
            matrix_from_sympy(H),
            "\\cdot",
            matrix_from_sympy(sol),
            " = ",
            rational_latex((sol.T * H * sol)[0])
        ]
        return Formula(formula_data)

    @formula
    def _fill_opt_objective_value(self):
        opt_X = solution_matrix(self.objective)
        formula_data = [
            "f(X^*) = ",
            rational_latex(self.objective.value(opt_X))
        ]
        return Formula(formula_data)
