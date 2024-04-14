import math

from tasks.qt.models.queueing_systems.limited_source_infinite_queue_qs import LimitedSourceInfiniteQueueQS


class LimitedSourceInfiniteQueueWithBoostQS(LimitedSourceInfiniteQueueQS):
    def __init__(self, k, lamb, mu, n, boost_limit, boost_size):
        if boost_limit <= k:
            raise ValueError("boost_limit <= k")
        super().__init__(k, lamb, mu, n)
        self.k = k
        self.lamb = lamb
        self.mu = mu
        self.n = n
        self.boost_limit = boost_limit
        self.boost_size = boost_size

    def P0(self):
        result = 1
        k = self.k
        n = self.n
        rho = self.lamb / self.mu
        rho_b = rho / self.boost_size
        for j in range(1, k + 1):
            result += rho ** j * math.factorial(n) / (math.factorial(j) * math.factorial(n - j))
        for j in range(k + 1, self.boost_limit + 1):
            result += rho ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k))
        for j in range(self.boost_limit + 1, n + 1):
            result += rho_b ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k))
        return result ** -1

    def Pj(self, j: int):
        rho = self.lamb / self.mu
        k = self.k
        n = self.n
        rho_b = rho / self.boost_size
        if j <= k:
            return rho ** j * math.factorial(n) / (math.factorial(j) * math.factorial(n - j)) * self.P0()
        if k < j <= self.boost_limit:
            return rho ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k)) * self.P0()
        else:
            return rho_b ** j * math.factorial(n) / (math.factorial(k) * math.factorial(n - j) * k ** (j - k)) * self.P0()
