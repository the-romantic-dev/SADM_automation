from tasks.task1_2_lp.model import BasisSolution
from tasks.task1_2_lp.model import LPProblem


def is_opt(sol: BasisSolution, is_reversed: bool) -> bool:
    result = sol.is_opt
    if is_reversed:
        result = sol.is_acceptable
    return result


def is_acceptable(sol: BasisSolution, is_reversed: bool) -> bool:
    result = sol.is_acceptable
    if is_reversed:
        result = sol.is_opt
    return result


def get_swap_indices(sol: BasisSolution, is_reversed: bool):
    c = sol.objective_coeffs
    b = sol.basis_values
    coeffs = sol.basis_coeffs
    if is_reversed:
        out_var_index = b.index(min(b))
        out_var_row = coeffs[out_var_index]

        column_criteria = [c[i] / -out_var_row[i] for i in range(len(c))]
        filtered_criteria = list(filter(lambda elem: elem > 0, column_criteria))
        in_var_index = column_criteria.index(min(filtered_criteria))
    else:
        in_var_index = c.index(max(c))
        in_var_column = [row[in_var_index] for row in coeffs]

        row_criteria = [b[i] / -in_var_column[i] for i in range(len(b))]
        filtered_criteria = list(filter(lambda elem: elem >= 0, row_criteria))
        out_var_index = row_criteria.index(min(filtered_criteria))
    return out_var_index, in_var_index


def get_next_basis(sol: BasisSolution, is_reversed: bool) -> tuple[list[int], list[int], tuple[int, int]] | None:
    if is_opt(sol, is_reversed) or not is_acceptable(sol, is_reversed):
        return None

    out_var_index, in_var_index = get_swap_indices(sol, is_reversed)

    old_basis = sol.basis
    old_free = sol.free
    new_basis: list = list(old_basis)
    new_basis[out_var_index] = old_free[in_var_index]

    new_free: list = list(old_free)
    new_free[in_var_index] = old_basis[out_var_index]

    swap = (old_basis[out_var_index], old_free[in_var_index])
    return new_basis, new_free, swap


class SymplexSolver:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def solve(self, start_basis: list[int] = None, is_reversed: bool = False):
        if start_basis is None:
            start_basis = self.lp_problem.start_basis
        curr_basis_solution = BasisSolution(self.lp_problem, start_basis)
        result = [curr_basis_solution]
        swaps = []
        while not is_opt(curr_basis_solution, is_reversed):
            new_basis, new_free, swap = get_next_basis(curr_basis_solution, is_reversed)
            swaps.append(swap)
            curr_basis_solution = BasisSolution(self.lp_problem, new_basis, new_free)
            result.append(curr_basis_solution)
        return result, swaps

    def auxiliary_solve(self):
        auxiliary_form = self.lp_problem.auxiliary_form
        curr_basis_solution = BasisSolution(auxiliary_form, auxiliary_form.start_basis)
        result = [curr_basis_solution]
        swaps = []

        def does_basis_contains_art_var(basis: list[int]):
            for b in basis:
                if b >= self.lp_problem.canonical_form.var_count:
                    return True
            return False

        while does_basis_contains_art_var(curr_basis_solution.basis):
            new_basis, new_free, swap = get_next_basis(curr_basis_solution, is_reversed=False)
            swaps.append(swap)
            curr_basis_solution = BasisSolution(auxiliary_form, new_basis, new_free)
            result.append(curr_basis_solution)

        return result, swaps
