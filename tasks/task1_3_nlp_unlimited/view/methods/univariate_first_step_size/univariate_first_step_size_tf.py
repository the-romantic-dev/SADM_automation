import math
from pathlib import Path

import numpy as np
from sympy import Matrix

from report.docx.omml import latex2omml
from report.model.docx_parts.formula import Formula
from report.model.elements.math.braces import braces, BraceType
from report.model.elements.util import get_element_from_xml_template
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import elements_list, formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod
from tasks.task1_3_nlp_unlimited.model.univariate_step_size_finder import UnivariateStepSizeFinder

template_path = Path(Path(__file__).parent, "univariate_first_step_size.docx")

steps_number_formula_xml_path = Path(Path(__file__).parent, "steps_number_formula_element.txt")


def float_str(num: float, rounding: int):
    return f"{num:.{rounding}f}".rstrip('0').rstrip('.')


class UnivariateFirstStepSizeTF(TemplateFiller):
    def __init__(self, method: IterativeMethod, start_point: Matrix):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        direction = method.step_direction(start_point, None, 0)
        self.finder = UnivariateStepSizeFinder(objective=method.objective, point=start_point, direction=direction)
        self.interval_steps = self.finder.start_interval_steps
        self.golden_section_steps = self.finder.golden_section_method_steps(
            (self.interval_steps[-3], self.interval_steps[-1])
        )

    @elements_list
    def _fill_uncertainty_interval_steps(self):
        steps = self.interval_steps

        def step_formula(i: int, step_size: float):
            step_formula_data = [
                f"t_{i}^{{(0)}} = {float_str(step_size, 4)}",
                r"\rightarrow",
                f"f", braces(latex2omml(f"X^{{(0)}} + t_{i}^{{(0)}}K^{{(0)}}")),
                f"= {float_str(self.finder.f(step_size), 4)}"
            ]
            return Formula(step_formula_data)

        formulas = [step_formula(i, steps[i]) for i in range(len(steps))]
        return formulas

    @formula
    def _fill_start_interval(self):
        left_elem_latex = float_str(self.interval_steps[-3], 4)
        right_elem_latex = float_str(self.interval_steps[-1], 4)
        formula_data = [
            braces(latex2omml(f"{left_elem_latex}, {right_elem_latex}"), BraceType.BRACKETS)
        ]
        return Formula(formula_data)

    @formula
    def _fill_golden_section_steps(self):
        def insert_between(lst, element):
            result = []
            for i in range(len(lst) - 1):
                result.append(lst[i])
                result.append(element)
            result.append(lst[-1])  # Добавляем последний элемент без вставки после него
            return result

        formula_data = [
            braces(latex2omml(f"{float_str(step[0], 4)}, {float_str(step[1], 4)}"), BraceType.BRACKETS)
            for step in self.golden_section_steps
        ]
        formula_data = insert_between(formula_data, r"\rightarrow")
        return Formula(formula_data)

    @formula
    def _fill_first_step_size(self):
        last_step = self.golden_section_steps[-1]
        formula_data = [
            "{t^{*}}^{(0)} = "
            f"\\frac{{{float_str(last_step[0], 4)} + {float_str(last_step[1], 4)}}}{{2}} = ",
            float_str((round(last_step[0], 4) + round(last_step[1], 4)) / 2, 5)
        ]
        return Formula(formula_data)

    @formula
    def _fill_steps_formula(self):
        left_bound = self.interval_steps[-3]
        right_bound = self.interval_steps[-1]
        distance = right_bound - left_bound
        left_bound_str = float_str(left_bound, 4)
        right_bound_str = float_str(right_bound, 4)
        tolerance_str = '0.001'
        p = float_str(math.log(distance / float(tolerance_str)), 4)
        q = float_str(math.log(1.618), 4)

        formula_data = [
            "N = ",
            get_element_from_xml_template(txt_path=steps_number_formula_xml_path,
                                          keys=['right_bound', 'left_bound', 'tolerance'],
                                          replacements=[right_bound_str, left_bound_str, tolerance_str]),
            ' = ',
            braces(
                latex2omml(f'\\frac{{{p}}}{{{q}}}'), BraceType.UP_ROUND
            ),
            f'= {int(float(p) / float(q)) + 1}'
        ]
        return Formula(formula_data)
