""" Модуль для решения ЗЛП методом полного перебора опорных точек """

import itertools
from dataclasses import dataclass
import sympy as sp

from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.solvers.util import LPPData, get_column


class BruteforceSolver:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def solve(self):
        total_vars = self.lp_problem.canonical_form.var_count
        result = []
        basises = list(itertools.combinations(range(total_vars), 2))
        opt_index = -1
        for i, basis in enumerate(reversed(basises)):
            solution = BasisSolution(lp_problem=self.lp_problem, basis=basis)
            result.append(solution)
            if solution.is_opt:
                opt_index = i
        return result, opt_index
