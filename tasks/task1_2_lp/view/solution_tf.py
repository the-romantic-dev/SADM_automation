from report.model.elements.formula import Formula
from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel


class SolutionTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate):
        super().__init__(template)

    @staticmethod
    def result_formula(opt_solution: BasisSolution):
        best_solution_vm = BasisSolutionViewModel(opt_solution)
        basis_variables = best_solution_vm.basis_variables_latex
        free_variables = best_solution_vm.free_variables_latex
        f_variable = 'f'
        variables = basis_variables + free_variables + [f_variable]

        basis_values = [rational_latex(value) for value in opt_solution.basis_values]
        free_values = ["0" for _ in range(len(opt_solution.free))]
        f_value = rational_latex(opt_solution.objective_value)
        values = basis_values + free_values + [f_value]

        formula_latex = ",".join(f"{variables[i]} = {values[i]}" for i in range(len(variables)))
        return Formula(formula_latex)
