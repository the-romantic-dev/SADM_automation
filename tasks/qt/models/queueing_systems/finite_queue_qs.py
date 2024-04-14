import math

from tasks.qt.models.queuing_system import QueuingSystem


class FiniteQueueQS(QueuingSystem):
    def __init__(self, k, m, lamb, mu):
        self.k = k
        self.m = m
        self.lamb = lamb
        self.mu = mu

    def P0(self):
        result = 1
        k = self.k
        m = self.m
        rho = self.lamb / self.mu
        rho_c = self.lamb / (k * self.mu)
        for j in range(1, k + 1):
            result += rho ** j / math.factorial(j)
        result += (rho ** (k + 1) * (1 - rho_c ** m)) / (math.factorial(k) * k * (1 - rho_c))
        return result ** -1

    def Pj(self, j: int):
        rho = self.lamb / self.mu
        k = self.k
        if j <= k:
            return rho ** j / math.factorial(j) * self.P0()
        else:
            return rho ** j / (math.factorial(k) * k ** (j - k)) * self.P0()

    def P_err(self):
        k = self.k
        m = self.m
        rho = self.lamb / self.mu
        return (rho ** (k + m) * self.P0()) / (k ** m * math.factorial(k))

    def n_o(self):
        k = self.k
        m = self.m
        rho = self.lamb / self.mu
        rho_c = self.lamb / (k * self.mu)
        factor = rho ** (k + 1) * self.P0()
        top = 1 - rho_c ** m * (m + 1 - rho_c * m)
        bottom = (math.factorial(k) * k * (1 - rho_c) ** 2)
        return factor * top / bottom

    def k3(self):
        rho = self.lamb / self.mu
        return rho * (1 - self.P_err())

    def j(self):
        return self.n_o() + self.k3()

    def t_wait(self):
        return self.n_o() / self.lamb

    def t_sys(self):
        return self.j() / self.lamb
