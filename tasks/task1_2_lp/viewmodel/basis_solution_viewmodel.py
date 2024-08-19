from sympy import latex

from report.model.report_prettifier import expr_latex
from tasks.task1_2_lp.model import BasisSolution


def variables_to_latex(variables):
    return [latex(x) for x in variables]


class BasisSolutionViewModel:
    def __init__(self, basis_solution: BasisSolution):
        self.basis_solution = basis_solution

    @property
    def basis_variables_latex(self) -> list[str]:
        return variables_to_latex(self.basis_solution.basis_variables)

    @property
    def free_variables_latex(self) -> list[str]:
        return variables_to_latex(self.basis_solution.free_variables)

    @property
    def basis_expressions_latex(self) -> list[str]:
        result = []
        basis_coeffs = self.basis_solution.basis_coeffs
        basis_variables = self.basis_solution.basis_variables
        free_variables = self.basis_solution.free_variables
        basis_values = self.basis_solution.basis_values
        for coeffs, constant, variable in zip(basis_coeffs, basis_values, basis_variables):
            result.append(f"{latex(variable)} = {expr_latex(coeffs, free_variables, constant)}")
        return result

    @property
    def f_expression_latex(self) -> str:
        coeffs = self.basis_solution.objective_coeffs
        variables = self.basis_solution.free_variables
        const = self.basis_solution.objective_value
        return f"f = {expr_latex(coeffs, variables, const)}"