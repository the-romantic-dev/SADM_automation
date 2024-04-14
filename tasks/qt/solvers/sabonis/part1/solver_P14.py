from tasks.qt.models.queueing_systems.impatient_finite_queue_qs import ImpatientFiniteQueueQS


class SolverP14:
    def __init__(self, n, a, b, d, m):
        self.lamb = m
        self.k = n
        self.m = d
        mu = 1 / (a / 60)
        nu = 1 / (b / 60)
        self.qs = ImpatientFiniteQueueQS(k=self.k, m=self.m, lamb=self.lamb, mu=mu, nu=nu)

    def solve(self):
        print(f"P_доз = {1 - self.qs.P_escape_queue() - self.qs.P_err()}")
        print(f"kз = {self.qs.k3()}")
        print(f"t_прост = {(self.k - self.qs.k3()) / self.lamb}")


solver = SolverP14(n=2, a=10, b=25, d=5, m=15)
solver.solve()
