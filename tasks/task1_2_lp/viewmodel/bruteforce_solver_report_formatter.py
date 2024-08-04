from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.solvers.bruteforce_solver.bruteforce_solver import BruteforceSolver


class BruteforceSolverReportFormatter:
    def __init__(self, bruteforce_solver: BruteforceSolver):
        self.bruteforce_solver = bruteforce_solver
