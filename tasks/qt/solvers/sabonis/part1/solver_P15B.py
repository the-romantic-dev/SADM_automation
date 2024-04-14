import math

from tasks.qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


class QSModelP15BInfinite:
    def __init__(self, rho_1, rho_2, rho_3, rho_4, k, m):
        self.rho_1 = rho_1
        self.rho_2 = rho_2
        self.rho_3 = rho_3
        self.rho_4 = rho_4
        self.factor_1 = rho_1 ** k / math.factorial(k)
        self.factor_2 = self.factor_1 * rho_2 ** (m - k) / k ** (m - k)
        self.factor_3 = self.factor_2 * self.rho_3 / k
        self.k = k
        self.m = m

    def P0(self):
        result = 1
        for j in range(1, self.k + 1):
            result += self.rho_1 ** j / math.factorial(j)
        for j in range(self.k + 1, self.m + 1):
            jk = j - self.k
            result += self.factor_1 * self.rho_2 ** jk / self.k ** jk

        result += self.factor_3

        result += self.factor_3 * self.rho_4 / (self.k - self.rho_4)
        return result ** -1

    def Pj(self, j):
        if j <= self.k:
            result = self.rho_1 ** j / math.factorial(j)
        elif j <= self.m:
            jk = j - self.k
            result = self.factor_1 * self.rho_2 ** jk / self.k ** jk
        elif j == self.m + 1:
            result = self.factor_3
        else:
            result = self.factor_3 * self.rho_4 ** (j - self.m - 1) / self.k ** (j - self.k)
        return result * self.P0()

    def queue_loading(self):
        result = 0
        k = self.k
        m = self.m
        factor_3 = self.factor_3
        P0 = self.P0()
        rho_4 = self.rho_4
        for j in range(k + 1, m + 2):
            result += (j - k) * self.Pj(j)
        result += factor_3 * rho_4 / (k - rho_4) * P0 * (k / (k - rho_4) + m - k + 1)
        return result

    def channels_loading(self):
        result = 0
        k = self.k
        before_k_probabilities_sum = 0
        for j in range(k + 1):
            before_k_probabilities_sum += self.Pj(j)
            result += j * self.Pj(j)
        result += (1 - before_k_probabilities_sum) * k
        return result

    def queue_average_time(self, average_lamb):
        return self.queue_loading() / average_lamb


class SolverP15B:
    def __init__(self, k, a, m):
        def finite_average_lamb():
            result = 0
            result += lamb_1 * sum(state_probabilities_1[:k + 1])
            result += lamb_2 * sum(state_probabilities_1[k + 1:m + 2])
            result += lamb_3 * sum(state_probabilities_1[m + 2:2 * m + 1])
            return result

        def infinite_average_lamb():
            result = 0
            result += lamb_1 * sum([self.qs_2.Pj(j) for j in range(k + 1)])
            result += lamb_2 * sum([self.qs_2.Pj(j) for j in range(k + 1, m + 2)])
            result += lamb_3 * self.qs_2.P0() * self.qs_2.factor_3 * rho_4 / (k - rho_4)
            return result

        lamb_1 = 1
        lamb_2 = 7 / 8
        lamb_3 = 1 / 2
        mu_1 = 1 / a
        mu_2 = 3 / 2 * mu_1

        rho_1 = lamb_1 / mu_1
        rho_2 = lamb_2 / mu_1
        rho_3 = lamb_2 / mu_2
        rho_4 = lamb_3 / mu_2

        traffic_intensities_1 = [
            *[lamb_1 / (mu_1 * (j + 1)) for j in range(k)],
            *[lamb_2 / (k * mu_1) for _ in range(m - k)],
            lamb_2 / (k * mu_2),
            *[lamb_3 / (k * mu_2) for _ in range(m + 2, 2 * m + 1)]
        ]
        state_probabilities_1 = calculate_probabilities(traffic_intensities_1)

        self.qs_1 = FiniteStateModelQS(
            state_probabilities=state_probabilities_1,
            arrival_rate=finite_average_lamb(),
            channel_count=k, queue_length=2 * m, source_limit=None
        )

        self.qs_2 = QSModelP15BInfinite(
            rho_1=rho_1, rho_2=rho_2, rho_3=rho_3, rho_4=rho_4,
            k=k, m=m
        )
        self.qs_2_lamb = infinite_average_lamb()
        print(f"mu_1 = {mu_1}")
        print(f"mu_2 = {mu_2}")
        print(f"rho_1 = {rho_1}")
        print(f"rho_2 = {rho_2}")
        print(f"rho_3 = {rho_3}")
        print(f"rho_4 = {rho_4}")

    def solve(self):
        print(f"Среднее число машин в очереди: {self.qs_1.queue_loading()} | {self.qs_2.queue_loading()}")
        print(f"Среднее число занятых колонок: {self.qs_1.channels_loading()} | {self.qs_2.channels_loading()}")
        print(
            f"Среднее время ожидания машин в очереди: {self.qs_1.queue_average_time()} | {self.qs_2.queue_average_time(self.qs_2_lamb)}")


solver = SolverP15B(k=5, a=4, m=5)
solver.solve()
