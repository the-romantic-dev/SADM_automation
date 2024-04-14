import math

from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS


def factor_impatient(j, k, beta):
    result = 1
    for n in range(1, j - k + 1):
        result *= k + beta * n
    return result


class ImpatientFiniteQueueQS(FiniteQueueQS):
    def __init__(self, k, m, lamb, mu, nu):
        super().__init__(k, m, lamb, mu)
        self.nu = nu

    def P0(self):
        result = 1
        k = self.k
        m = self.m
        beta = self.nu / self.mu
        rho = self.lamb / self.mu
        for j in range(1, k + 1):
            result += rho ** j / math.factorial(j)
        for j in range(k + 1, m + k + 1):
            result += rho ** j / (math.factorial(k) * factor_impatient(j, k, beta))
        return result ** -1

    def n_o(self):
        result = 0
        k = self.k
        m = self.m
        for j in range(k + 1, m + k + 1):
            result += (j - k) * self.Pj(j)
        return result

    def Pj(self, j: int):
        k = self.k
        rho = self.lamb / self.mu
        beta = self.nu / self.mu
        if j <= k:
            return rho ** j / math.factorial(j) * self.P0()
        else:
            return rho ** j / (math.factorial(k) * factor_impatient(j, k, beta)) * self.P0()

    def P_err(self):
        return self.Pj(self.k + self.m)

    def k3(self):
        result = 0
        k = self.k
        m = self.m
        for j in range(1, k + 1):
            result += j * self.Pj(j)
        for j in range(1, m + 1):
            result += k * self.Pj(k + j)
        return result

    def P_escape_queue(self):
        eta = self.lamb / self.n_o()
        return math.e ** (-eta / self.nu)

    def P_escape(self):
        eta = 1 / self.t_sys()
        T = 1 / self.nu
        return math.e ** -(eta * T)

    def t_wait(self):
        return self.n_o() / self.lamb
