import math

from tasks.task2_3_qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.task2_3_qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


class QSModelP15BInfinite:
    def __init__(self, lamb_1, mu_1, mu_2, k, m, probabs_num):
        self.rho_1 = lamb_1 / mu_1
        self.lamb_1 = lamb_1
        self.rho_2 = lamb_1 / mu_2
        self.k = k
        self.m = m
        self.probabs_num = probabs_num
        summ = sum([self.Pj(j) for j in range(self.probabs_num)])
        print(summ)

    def traffic_intensity(self, j):
        if j == 0:
            return 1
        k = self.k
        m = self.m
        if j <= self.k:
            result = self.rho_1 / j
        elif k < j <= k + m:
            result = self.rho_1 / k
        else:
            result = self.rho_2 / k
        return result

    def P0(self):
        result = 0
        ti_list = []
        for j in range(self.probabs_num):
            ti = self.traffic_intensity(j)
            ti_list.append(ti)
            prod = math.prod(ti_list)
            result += prod
        return result ** -1

    def Pj(self, j):
        prod = math.prod([self.traffic_intensity(i) for i in range(j + 1)])
        return prod * self.P0()

    def queue_loading(self):
        k = self.k
        result = 0
        for j in range(k + 1, self.probabs_num):
            result += (j - k) * self.Pj(j)
        return result

    def channels_loading(self):
        k = self.k
        result = 0
        for j in range(1, k + 1):
            result += j * self.Pj(j)
        for j in range(k + 1, self.probabs_num):
            result += k * self.Pj(j)
        return result

    def queue_average_time(self):
        return self.queue_loading() / self.lamb_1


class SolverP15B:
    def __init__(self, k, a, m):
        def finite_average_lamb():
            result = 0
            result += lamb_1 * sum(state_probabilities_1[:k + 1])
            result += lamb_2 * sum(state_probabilities_1[k + 1:m + 2])
            result += lamb_3 * sum(state_probabilities_1[m + 2:])
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
            *[rho_1 / j for j in range(1, k + 1)],
            *[rho_2 / k for _ in range(m)],
            rho_3 / k,
            *[rho_4 / k for _ in range(m)]
        ]
        state_probabilities_1 = calculate_probabilities(traffic_intensities_1)

        self.qs_1 = FiniteStateModelQS(
            state_probabilities=state_probabilities_1,
            arrival_rate=finite_average_lamb(),
            channel_count=k, queue_length=2 * m + 1, source_limit=None
        )

        self.qs_2 = QSModelP15BInfinite(
            lamb_1=lamb_1, mu_1=mu_1, mu_2=mu_2,
            k=k, m=m, probabs_num=30
        )
        self.qs_2_lamb = lamb_1
        # print(f"mu_1 = {mu_1}")
        # print(f"mu_2 = {mu_2}")
        # print(f"rho_1 = {rho_1}")
        # print(f"rho_2 = {rho_2}")
        # print(f"rho_3 = {rho_3}")
        # print(f"rho_4 = {rho_4}")

    def solve(self):
        print(f"Среднее число машин в очереди: {self.qs_1.queue_loading()} | {self.qs_2.queue_loading()}")
        print(f"Среднее число занятых колонок: {self.qs_1.channels_loading()} | {self.qs_2.channels_loading()}")
        print(
            f"Среднее время ожидания машин в очереди: {self.qs_1.queue_average_time()} | {self.qs_2.queue_average_time()}")


solver = SolverP15B(k=5, a=4, m=5)
solver.solve()
