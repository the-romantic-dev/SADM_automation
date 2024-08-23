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

        basis = opt_solution.basis
        free = opt_solution.free
        total_vars = len(basis) + len(free)

        basis_variables = best_solution_vm.basis_variables_latex
        free_variables = best_solution_vm.free_variables_latex
        variables = []

        basis_values = [rational_latex(value) for value in opt_solution.basis_values]
        free_values = ["0" for _ in range(len(opt_solution.free))]
        values = []
        for i in range(total_vars):
            if i in basis:
                bi = basis.index(i)
                variables.append(basis_variables[bi])
                values.append(basis_values[bi])
            else:
                fi = free.index(i)
                variables.append(free_variables[fi])
                values.append(free_values[fi])

        variables += ['f']
        values += [rational_latex(opt_solution.objective_value)]

        formula_latex = ",".join(f"{variables[i]} = {values[i]}" for i in range(len(variables)))
        return Formula(formula_latex)
