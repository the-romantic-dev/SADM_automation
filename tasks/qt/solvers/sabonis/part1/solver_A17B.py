import math

from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS


class A17BQS(FiniteQueueQS):
    def __init__(self, k, m, lamb, mu, l):
        super().__init__(k, m, lamb, mu)
        self.l = l

    def P0(self):
        result = 1
        k = self.k
        l = self.l
        m = self.m
        rho = self.lamb / self.mu
        for g in range(k):
            for j in range(g * l + 1, (g + 1) * l + 1):
                result += rho ** j / (math.factorial(g) ** l * (g + 1) ** j)
        for j in range(k * l + 1, k + m + 1):
            result += rho ** j / (math.factorial(k) ** l * k ** (j - k * l))
        return result ** -1

    def Pj(self, j):
        if j == 0:
            return self.P0()
        k = self.k
        l = self.l
        m = self.m
        rho = self.lamb / self.mu
        for g in range(k):
            for j_temp in range(g * l + 1, (g + 1) * l + 1):
                if j_temp == j:
                    return rho ** j_temp / (math.factorial(g) ** l * (g + 1) ** j_temp) * self.P0()
        for j_temp in range(k * l + 1, k + m + 1):
            if j_temp == j:
                return rho ** j_temp / (math.factorial(k) ** l * k ** (j_temp - k * l)) * self.P0()

    def n_o(self):
        result = 0
        k = self.k
        l = self.l
        m = self.m
        for g in range(k):
            for j in range(g * l + 1, (g + 1) * l + 1):
                result += self.Pj(j) * (j - g - 1)
        for j in range(k * l + 1, m + 1):
            result += self.Pj(j) * (j - k * l)
        return result

    def P_err(self):
        return self.Pj(self.k + self.m)

class SolverA17B:
    def __init__(self, lamb, k, l, t, m):
        lamb = lamb
        mu = 1 / (t / 60)
        self.k = k
        self.m = m
        self.rho = lamb / mu
        self.qs = A17BQS(k=k, lamb=lamb, mu=mu, m=m, l=l)

    def solve(self):
        pjs = []
        for j in range(self.k + self.m + 1):
            pjs.append(self.qs.Pj(j))
            print(f"P{j} = {self.qs.Pj(j)}")
        print(sum(pjs))
        print(f"n_o = {self.qs.n_o()}")
        print(f"P_отк = {self.qs.P_err()}")


solver = SolverA17B(lamb=5, k=2, l=3, t=20, m=12)
solver.solve()