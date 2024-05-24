import sympy as sp

from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
from tasks.qt.solvers.sabonis.part2.wait_and_system_time_qs_comparator import WaitAndSystemTimeQSComparator


class Solver84(WaitAndSystemTimeQSComparator):
    def __init__(self, k, m):
        lamb = sp.symbols("λ")
        mu = sp.symbols("μ")
        qs1 = FiniteQueueQS(k=k, m=m, lamb=lamb, mu=mu)
        qs2 = FiniteQueueQS(k=k + 1, m=m - 3, lamb=lamb, mu=mu)
        super().__init__(qs1, qs2, k, k)


solver = Solver84(k=3, m=6)
solver.solve()
