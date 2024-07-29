import math

from tasks.task2_3_qt.models.queuing_system import QueuingSystem


class InfiniteQueueQS(QueuingSystem):
    def __init__(self, k, lamb, mu):
        self.k = k
        self.lamb = lamb
        self.mu = mu

    def P0(self):
        result = 1
        k = self.k
        rho = self.lamb / self.mu
        for j in range(1, k + 1):
            result += rho ** j / math.factorial(j)
        result += rho ** (k + 1) / (math.factorial(k) * (k - rho))
        return result ** -1

    def Pj(self, j: int):
        rho = self.lamb / self.mu
        k = self.k
        if j <= k:
            return rho ** j / math.factorial(j) * self.P0()
        else:
            return rho ** j / (math.factorial(k) * k ** (j - k)) * self.P0()

    def n_o(self):
        rho = self.lamb / self.mu
        k = self.k
        rho_c = self.lamb / (k * self.mu)
        return rho ** (k + 1) * self.P0() / (math.factorial(k) * k * (1 - rho_c) ** 2)

    def k3(self):
        rho = self.lamb / self.mu
        return rho

    def j(self):
        return self.n_o() + self.k3()

    def t_wait(self):
        return self.n_o() / self.lamb

    def t_sys(self):
        return self.j() / self.lamb
