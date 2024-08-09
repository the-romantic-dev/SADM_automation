from sympy import Rational, Matrix

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator


def constraint_value(coeffs, sol):
    x_values = sol.solution
    return sum([c * x for c, x in zip(coeffs, x_values)])


def round_rational_to_decimal(rat: Rational, decimals=1):
    mult = 10 ** decimals
    result = Rational(round(rat * mult), mult)
    return result


def neighbor_edge_center(opt: BasisSolution, neighbor: BasisSolution):
    opt_value = opt.solution
    neighbor_value = neighbor.solution
    center = [(o + n) / 2 for o, n in zip(opt_value, neighbor_value)]
    return center


class ReverseSymplexViewModel:
    def __init__(self, solutions: list[BasisSolution]):
        opt_sol = None
        acceptable_sols = []
        for sol in solutions:
            if sol.is_opt:
                opt_sol = sol
            elif sol.is_acceptable:
                acceptable_sols.append(sol)
        if opt_sol is None:
            raise ValueError("Нет оптимального базиса")
        self.opt_sol = opt_sol
        self.acceptable_sols = acceptable_sols
        self.coeffs = [Rational(0) for _ in range(sol.lp_problem.canonical_form.var_count)]
        self.coeffs[0] = Rational(1)

    @property
    def new_constraint(self):
        var_count = self.opt_sol.lp_problem.canonical_form.var_count
        neighbors = self.opt_neighbor_solutions
        opt = self.opt_sol
        new_constraint_coeffs = Matrix([Rational(0) for _ in range(var_count)])
        new_constraint_value = Rational(0)
        for neigh in neighbors:
            center = Matrix(neighbor_edge_center(opt, neigh))
            normal = Matrix([o - n for o, n in zip(opt.solution, neigh.solution)])
            new_constraint_coeffs += normal
            new_constraint_value += (normal * center.T)[0, 0]

        new_constraint_coeffs /= len(neighbors)
        new_constraint_value /= len(neighbors)

        coeffs_list = new_constraint_coeffs.T.tolist()[0]
        for i, coef in enumerate(coeffs_list):
            coeffs_list[i] = round_rational_to_decimal(coef)

        const = round_rational_to_decimal(new_constraint_value)
        return Constraint(coeffs=coeffs_list[:2], const=const,
                          comp_operator=CompOperator.LE)

        # # edge_centers = [neighbor_edge_center(opt, neighbor) for neighbor in neighbors]
        #
        # coeffs = self.coeffs
        # opt_constraint_value = constraint_value(coeffs, self.opt_sol)
        # b = opt_constraint_value - delta

    @property
    def opt_neighbor_solutions(self) -> list[BasisSolution]:
        def is_basis_neighbors(basis_1: list[int], basis_2: list[int]) -> bool:
            if len(basis_1) != len(basis_2):
                return False
            diff_count = 0
            for b1, b2 in zip(basis_1, basis_2):
                if b1 != b2:
                    diff_count += 1
                if diff_count > 1:
                    return False
            return diff_count == 1

        neighbors = []
        for sol in self.acceptable_sols:
            if is_basis_neighbors(self.opt_sol.basis, sol.basis):
                neighbors.append(sol)
        return neighbors

    @property
    def find_neighbor_edge_center(self):
        edge_centers
