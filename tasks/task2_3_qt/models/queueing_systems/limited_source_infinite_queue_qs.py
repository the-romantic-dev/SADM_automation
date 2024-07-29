import math

from tasks.task2_3_qt.models.queuing_system import QueuingSystem


class LimitedSourceInfiniteQueueQS(QueuingSystem):
    def __init__(self, k, lamb, mu, n):
        self.k = k
        self.lamb = lamb
        self.mu = mu
        self.n = n

    def P0(self):
        result = 1
        k = self.k
        n = self.n
        rho = self.lamb / self.mu
        for j in range(1, k + 1):
            result += rho ** j * math.factorial(n) / (math.factorial(j) * math.factorial(n - j))
        for j in range(k + 1, n + 1):
            result += rho ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k))
        return result ** -1

    def Pj(self, j: int):
        rho = self.lamb / self.mu
        k = self.k
        n = self.n
        if j <= k:
            return rho ** j * math.factorial(n) / (math.factorial(j) * math.factorial(n - j)) * self.P0()
        else:
            return rho ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k)) * self.P0()

    def n_o(self):
        result = 0
        k = self.k
        n = self.n
        for j in range(k + 1, n + 1):
            result += (j - k) * self.Pj(j)
        return result

    def k3(self):
        result = 0
        k = self.k
        n = self.n
        for j in range(1, k):
            result += j * self.Pj(j)
        for j in range(k, n + 1):
            result += k * self.Pj(j)
        return result

    def j(self):
        return self.n_o() + self.k3()

    def t_wait(self):
        n = self.n
        return self.n_o() / (self.lamb * (n - self.j()))

    def t_sys(self):
        n = self.n
        return self.j() / (self.lamb * (n - self.j()))
