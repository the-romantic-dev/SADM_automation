from copy import copy

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem


def get_next_basis(basis_solution: BasisSolution) -> tuple[tuple, tuple, tuple] | None:
    if basis_solution.is_opt or not basis_solution.is_acceptable:
        return None

    obj_coeffs = basis_solution.objective_coeffs
    in_var_index = obj_coeffs.index(max(obj_coeffs))
    basis_values = basis_solution.basis_values
    basis_coeffs = basis_solution.basis_coeffs
    in_var_column = [row[in_var_index] for row in basis_coeffs]

    row_criteria = [basis_values[i] / -in_var_column[i] for i in range(len(basis_values))]
    filtered_non_negative_rc = list(filter(lambda elem: elem >= 0, row_criteria))
    out_var_index = row_criteria.index(min(filtered_non_negative_rc))

    old_basis = basis_solution.basis
    old_free = basis_solution.free
    new_basis: list = list(old_basis)
    new_basis[out_var_index] = old_free[in_var_index]

    new_free: list = list(old_free)
    new_free[in_var_index] = old_basis[out_var_index]

    swap = (old_basis[out_var_index], old_free[in_var_index])
    return tuple(new_basis), tuple(new_free), swap


# def basis_different(basis_1, basis_2):
#     for i in range(len(basis_1)):
#         if basis_1[i] != basis_2[i]:
#             return basis_1[i], basis_2[i]
#     return None


class SymplexSolver:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def solve(self):
        curr_basis_solution = BasisSolution(self.lp_problem, self.lp_problem.start_basis)
        result = [curr_basis_solution]
        swaps = []
        while not curr_basis_solution.is_opt:
            new_basis, new_free, swap = get_next_basis(curr_basis_solution)
            swaps.append(swap)
            curr_basis_solution = BasisSolution(self.lp_problem, new_basis, new_free)
            result.append(curr_basis_solution)
        return result, swaps
