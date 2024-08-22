import os
from pathlib import Path

from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.elements.formula import Formula
from report.model.template.filler_decorators import text, elements_list, formula, document
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel
from tasks.task1_2_lp.view.bruteforce_solution.bruteforce_step.acceptability_marker.acceptability_marker_tf import \
    AcceptabilityMarkerTF
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "bruteforce_step.docx")


@sub_tf
class BruteforceStepTF(TemplateFiller):
    def __init__(self, solution_index: int, basis_solution: BasisSolution):
        self.basis_solution = basis_solution
        self.basis_solution_vm = BasisSolutionViewModel(basis_solution)
        self.solution_index = solution_index
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @text
    def _fill_solution_index(self):
        return str(self.solution_index + 1)

    @formula
    def _fill_basis_variables(self):
        formula_latex = ",".join(self.basis_solution_vm.basis_variables_latex)
        return Formula(formula_latex)

    @elements_list
    def _fill_expressions(self):
        basis_expressions = self.basis_solution_vm.basis_expressions_latex
        formulas_list = [Formula(expr_latex) for expr_latex in basis_expressions]
        formulas_list.append(Formula(self.basis_solution_vm.f_expression_latex))
        return formulas_list

    @elements_list
    def _fill_values(self):
        basis_values = self.basis_solution.basis_values
        objective_value = self.basis_solution.objective_value
        basis_variables = self.basis_solution_vm.basis_variables_latex
        variables = [*basis_variables, 'f']
        values = [rational_latex(const) for const in [*basis_values, objective_value]]
        return [Formula(f"{var} = {val}") for var, val in zip(variables, values)]

    @document
    def _fill_acceptable_marker(self):
        if self.basis_solution.is_acceptable:
            return None
        acceptability_marker_tf = AcceptabilityMarkerTF(
            unacceptable_variables=self.basis_solution.unacceptable_variables
        )
        acceptability_marker_tf.fill()
        return acceptability_marker_tf.template.document
