import math

from tasks.task2_3_qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
from tasks.task2_3_qt.models.queueing_systems.limited_source_infinite_queue_with_boost_qs import \
    LimitedSourceInfiniteQueueWithBoostQS
from tasks.task2_3_qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.task2_3_qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


class QSAC9:
    def __init__(self, n, k, m, r):
        self.lamb = k
        self.mu = m
        self.n = n
        self.r = r

    def rho(self, i, j):
        return (self.n - j) * self.lamb / (i * self.mu)

    def P0(self):
        result = 1
        result += sum([math.prod([self.rho(k, j) for k in range(1, j + 1)]) for j in range(1, self.r + 1)])
        result += sum(
            [math.prod([self.rho(self.r, j) for k in range(1, j + 1)]) for j in range(self.r + 1, 2 * self.r + 1)])
        result += sum([math.prod([0.8 * self.rho(self.r, j) for k in range(1, j + 1)]) for j in
                       range(2 * self.r + 1, self.n + 1)])
        return result ** -1

    def Pj(self, j):
        if j <= self.r:
            return math.prod([self.rho(k, j) for k in range(1, j + 1)]) * self.P0()
        elif j <= self.r * 2:
            return math.prod([self.rho(self.r, j) for k in range(1, j + 1)]) * self.P0()
        else:
            return math.prod([0.8 * self.rho(self.r, j) for k in range(1, j + 1)]) * self.P0()

    def n_o(self):
        return sum([self.Pj(j) * (j - self.r) for j in range(self.r + 1, self.n)])

    def k3(self):
        result = 0
        result += sum([self.Pj(j) * j for j in range(1, self.r)])
        result += sum([self.Pj(j) for j in range(self.r, self.n + 1)]) * self.r
        return result

    def j(self):
        return self.n_o() + self.k3()

    def t_sys(self):
        return self.j() / (self.lamb * (self.n - self.j()))

    def t_wait(self):
        return self.n_o() / (self.lamb * (self.n - self.j()))


class SolverAC9:
    def __init__(self, n, k, m, r):
        lamb = k
        mu_1 = m
        mu_2 = mu_1 * 1.25
        self.n = n
        self.r = r
        traffic_intensities = [
            *[lamb * (n - j) / (mu_1 * (j + 1)) for j in range(r)],
            *[lamb * (n - j) / (r * mu_1) for j in range(r, 2 * r)],
            *[lamb * (n - j) / (r * mu_2) for j in range(2 * r, n)],
        ]
        state_probabilities = calculate_probabilities(traffic_intensities)
        self.qs = FiniteStateModelQS(
            state_probabilities=state_probabilities,
            arrival_rate=lamb,
            channel_count=r,
            queue_length=None,
            source_limit=n
        )

    def solve(self):
        for j in range(self.qs.source_limit + 1):
            print(f"P{j} = {self.qs.state_probability(j)}")
        print(f"n_o = {self.qs.queue_loading()}")
        print(f"kз = {self.qs.channels_loading()}")
        print(f"j = {self.qs.system_loading()}")
        print(f"t_с = {self.qs.system_average_time()}")
        print(f"t_ож = {self.qs.queue_average_time()}")


solver = SolverAC9(n=10, k=0.05, m=0.5, r=1)
solver.solve()
