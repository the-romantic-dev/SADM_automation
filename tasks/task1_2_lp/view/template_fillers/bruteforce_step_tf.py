from pathlib import Path

from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.elements.formula import Formula
from report.model.template.filler_decorators import text, elements_list, formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel
from tasks.task1_2_lp.view.template_fillers.acceptability_marker_tf import AcceptabilityMarkerTF
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution


class BruteforceStepTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, solution_index: int, basis_solution: BasisSolution):
        self.basis_solution = basis_solution
        self.basis_solution_vm = BasisSolutionViewModel(basis_solution)
        self.solution_index = solution_index
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
        # basis_expressions = [replace_rationals_expr(expr) for expr in self.basis_solution._express_basis_through_free]
        basis_expressions = self.basis_solution_vm.basis_expressions_latex
        # basis_variables = self.basis_solution.basis_variables_latex
        formulas_list = [Formula(expr_latex) for expr_latex in basis_expressions]
        # for i, variable in enumerate(basis_variables):
        #     formula = Formula(eq_latex(variable, basis_expressions[i]))
        #     formulas_list.append(formula)
        formulas_list.append(Formula(self.basis_solution_vm.f_expression_latex))
        # expr = replace_rationals_expr(self.basis_solution._express_objective_through_free)
        # objective_formula = Formula(eq_latex(f, expr))
        # formulas_list.append(objective_formula)
        return formulas_list

    @elements_list
    def _fill_values(self):
        basis_values = self.basis_solution.basis_values
        objective_value = self.basis_solution.objective_value
        basis_variables = self.basis_solution_vm.basis_variables_latex
        variables = [*basis_variables, 'f']
        values = [rational_latex(const) for const in [*basis_values, objective_value]]
        return [Formula(f"{var} = {val}") for var, val in zip(variables, values)]

    @TemplateFiller.filler_method
    def _fill_acceptable_marker(self):
        template_path = Path(TASK_DIR, "_templates/sabonis/bruteforce/acceptability_marker.docx")
        acceptability_marker_tf = AcceptabilityMarkerTF(
            template=DocumentTemplate(template_path),
            unacceptable_variables=self.basis_solution.unacceptable_variables
        )
        key = "acceptable_marker"
        if self.basis_solution.is_acceptable:
            self.template.delete_key(key)
        else:
            acceptability_marker_tf.fill()
            filled_document = acceptability_marker_tf.template.document
            self.template.insert_data_from_document(key=key, document=filled_document)
