from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem


def get_next_basis(basis_solution: BasisSolution) -> list[int] | None:
    if basis_solution.is_opt or not basis_solution.is_acceptable:
        return None

    obj_coeffs = basis_solution.objective_expression_coeffs
    in_var_index = obj_coeffs.index(max(obj_coeffs))
    basis_values = basis_solution.basis_values
    basis_coeffs = basis_solution.basis_expression_coeffs
    in_var_column = [row[in_var_index] for row in basis_coeffs]

    row_criteria = [basis_values[i] / -in_var_column[i] for i in range(len(basis_values))]
    filtered_non_negative_rc = list(filter(lambda elem: elem >= 0, row_criteria))
    out_var_index = row_criteria.index(min(filtered_non_negative_rc))

    old_basis = basis_solution.basis
    old_free = basis_solution.free
    new_basis = list(old_basis)
    new_basis[out_var_index] = old_free[in_var_index]
    return new_basis


class SymplexSolver:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def solve(self):
        curr_basis_solution = BasisSolution(self.lp_problem, self.lp_problem.start_basis)
        result = [curr_basis_solution]
        while not curr_basis_solution.is_opt:
            new_basis = get_next_basis(curr_basis_solution)
            curr_basis_solution = BasisSolution(self.lp_problem, new_basis)
            result.append(curr_basis_solution)
        return result
