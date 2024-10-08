""" Модуль для решения ЗЛП методом полного перебора опорных точек """

import itertools

from tasks.task1_2_lp.model import BasisSolution, LPProblem


class BruteforceSolver:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem
        self._solution = None

    def solve(self):
        if self._solution is not None:
            return self._solution
        total_vars = self.lp_problem.canonical_form.var_count
        result = []
        basises = list(itertools.combinations(range(total_vars), 2))
        opt_index = -1
        for i, basis in enumerate(reversed(basises)):
            solution = BasisSolution(lp_problem=self.lp_problem, basis=basis)
            result.append(solution)
            if solution.is_opt and solution.is_acceptable:
                opt_index = i
        self._solution = result, opt_index
        return result, opt_index
