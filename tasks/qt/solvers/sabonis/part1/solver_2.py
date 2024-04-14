import math

from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
from tasks.qt.models.queueing_systems.impatient_finite_queue_qs import ImpatientFiniteQueueQS
from tasks.qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


class QS2:
    def __init__(self, t, k, m, n):
        self.lamb = 10
        self.mu = k
        self.nu = 1 / t
        self.n = n
        self.m = m

    def rho(self, i, j):
        return self.lamb / (i * self.mu + j * self.nu)

    def Pj(self, j):
        if j <= self.n:
            return math.prod([self.rho(k, k) for k in range(1, j + 1)]) * self.P0()
        else:
            return math.prod([self.rho(self.n, k) for k in range(1, j + 1)]) * self.P0()

    def P0(self):
        result = 1
        result += sum([math.prod([self.rho(k, k) for k in range(1, j + 1)]) for j in range(1, self.n + 1)])
        result += sum([math.prod([self.rho(self.n, k) for k in range(1, j + 1)]) for j in range(1, self.n + 1)])
        return result ** -1

    def P_err(self):
        return self.Pj(self.n + self.m)

    def k3(self):
        result = 0
        result += sum([self.Pj(j) * j for j in range(1, self.n)])
        result += sum([self.Pj(j) * self.n for j in range(self.n, self.n + self.m + 1)])
        return result

    def n_o(self):
        result = 0
        result += sum([self.Pj(self.n + j) * j for j in range(1, self.m + 1)])
        return result

    def P_escape(self):
        eta = self.lamb / (self.n_o() + self.k3())
        return math.e ** (-eta / self.nu)
class Solver2:
    def __init__(self, t, k, m, n):
        self.lamb = 10
        self.mu = k
        self.nu = 1 / t
        # self.impatient_qs = QS2(t, k, m, n)

        traffic_intensities = [
            *[self.lamb / (self.mu * (j + 1) + self.nu * (j + 1)) for j in range(n)],
            *[self.lamb / (n * self.mu + (n + j + 1) * self.nu) for j in range(m)]
        ]
        self.states_num = m + n + 1
        state_probabilities = calculate_probabilities(traffic_intensities)
        self.impatient_qs = FiniteStateModelQS(
            state_probabilities=state_probabilities,
            arrival_rate=self.lamb,
            channel_count=n,
            queue_length=m,
            source_limit=None
        )
        self.patient_qs = FiniteQueueQS(k=n, m=m, lamb=self.lamb, mu=self.mu)

    def solve(self):
        print(f"nu = {self.nu}")
        print(f"mu = {self.mu}")
        for j in range(self.states_num):
            print(f"P{j} = {self.impatient_qs.state_probability(j)} | {self.patient_qs.Pj(j)}")
        print(f"n_o = {self.impatient_qs.queue_loading()} | {self.patient_qs.n_o()}")
        print(f"kз = {self.impatient_qs.channels_loading()} | {self.patient_qs.k3()}")
        print(f"P_отк = {self.impatient_qs.state_probability(-1)} | {self.patient_qs.P_err()}")
        queue_escape_probability = self.impatient_qs.queue_loading() * self.nu / self.lamb
        channel_escape_probability = self.impatient_qs.channels_loading() * self.nu / self.lamb
        print(f"P'_пот = {channel_escape_probability}")
        print(f"P''_пот = {queue_escape_probability}")
        print(f"P_пот = {queue_escape_probability + channel_escape_probability}")
        print(f"P_н.о = {queue_escape_probability + channel_escape_probability + self.impatient_qs.state_probability(-1)}")


solver = Solver2(t=2, k=10, m=3, n=2)
solver.solve()
