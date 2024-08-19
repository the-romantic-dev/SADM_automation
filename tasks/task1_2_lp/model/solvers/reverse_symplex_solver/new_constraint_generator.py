from sympy import Rational, Matrix, gcd

from tasks.task1_2_lp.model import BasisSolution
from tasks.task1_2_lp.model import Constraint


def __constraint_value(coeffs, sol):
    x_values = sol.solution
    return sum([c * x for c, x in zip(coeffs, x_values)])


def __round_rational_to_decimal(rat: Rational, decimals=0):
    mult = 10 ** decimals
    result = Rational(round(rat * mult), mult)
    return result


def __neighbor_edge_center(opt: BasisSolution, neighbor: BasisSolution):
    opt_value = opt.solution
    neighbor_value = neighbor.solution
    center = [(o + n) / 2 for o, n in zip(opt_value, neighbor_value)]
    return center


def __is_basis_neighbors(basis_1: list[int], basis_2: list[int]) -> bool:
    if len(basis_1) != len(basis_2):
        return False
    diff_count = 0
    for b1, b2 in zip(basis_1, basis_2):
        if b1 != b2:
            diff_count += 1
        if diff_count > 1:
            return False
    return diff_count == 1


def __opt_neighbors(opt_basis: list[int], acceptable_solutions: list[BasisSolution]) -> list[BasisSolution]:
    neighbors = []
    for sol in acceptable_solutions:
        if __is_basis_neighbors(opt_basis, sol.basis):
            neighbors.append(sol)
    return neighbors


def get_acceptable_and_opt_solutions(solutions: list[BasisSolution]):
    opt_sol = None
    acceptable_sols = []
    for sol in solutions:
        if sol.is_opt:
            opt_sol = sol
        elif sol.is_acceptable:
            acceptable_sols.append(sol)
    return acceptable_sols, opt_sol


def __new_coeffs_and_const(var_count: int, opt: BasisSolution, opt_neighbors: list[BasisSolution]):
    new_constraint_coeffs = Matrix([Rational(0) for _ in range(var_count)])
    new_constraint_value = Rational(0)
    for neigh in opt_neighbors:
        center = Matrix(__neighbor_edge_center(opt, neigh))
        normal = Matrix([o - n for o, n in zip(opt.solution, neigh.solution)])
        new_constraint_coeffs += normal
        new_constraint_value += (normal * center.T)[0, 0]

    original_var_count = opt.lp_problem.var_count
    new_constraint_coeffs /= len(opt_neighbors)
    new_constraint_coeffs = new_constraint_coeffs.T.tolist()[0][:original_var_count]

    new_constraint_value /= len(opt_neighbors)

    return new_constraint_coeffs, new_constraint_value


def generate_new_constraint(solutions: list[BasisSolution]):
    acceptable_sols, opt_sol = get_acceptable_and_opt_solutions(solutions)
    canonical_var_count = opt_sol.lp_problem.canonical_form.var_count

    neighbors = __opt_neighbors(opt_basis=opt_sol.basis, acceptable_solutions=acceptable_sols)

    coeffs, const = __new_coeffs_and_const(var_count=canonical_var_count, opt=opt_sol, opt_neighbors=neighbors)

    for i, coeff in enumerate(coeffs):
        coeffs[i] = __round_rational_to_decimal(coeff)

    const = __round_rational_to_decimal(const)
    _gcd = gcd([*coeffs, const])

    coeffs = [c / _gcd for c in coeffs]
    const /= _gcd
    return Constraint(coeffs=coeffs, const=const)
