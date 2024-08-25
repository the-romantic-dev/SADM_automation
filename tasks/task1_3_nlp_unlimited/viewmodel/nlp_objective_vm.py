from lxml.etree import _Element

from report.docx.omml import latex2omml
from report.model.elements.math.braces import braces
from report.model.report_prettifier import expr_latex
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective


def nlp_objective_element(nlp_objective: NLPObjective) -> _Element:
    ltx = expr_latex(coeffs=nlp_objective.coeffs, variables=[
        "x_1^2", "x_2^2", "x_1 x_2", "x_1", "x_2"
    ])
    return braces(latex2omml(ltx))

# class NLPObjectiveViewModel:
#     def __init__(self, nlp_objective: NLPObjective):
#         self.nlp_objective = nlp_objective

