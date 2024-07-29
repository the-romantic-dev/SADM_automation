import math

from tasks.task2_3_qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS
from tasks.task2_3_qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.task2_3_qt.models.queueing_systems.probabilities_calculator import calculate_probabilities

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
            result += lamb_2 * sum(state_probabilities_1[k + 1:k + m + 2])
            result += lamb_3 * sum(state_probabilities_1[k + m + 2:k + 2*m + 2])
            return result

        lamb_1 = 1
        lamb_2 = 7 / 8
        lamb_3 = 1 / 2
        mu_1 = 1 / a

        rho_1 = lamb_1 / mu_1
        rho_2 = lamb_2 / mu_1
        rho_3 = lamb_3 / mu_1

        traffic_intensities_1 = [
            *[rho_1 / j for j in range(1, k + 1)],
            *[rho_2 / k for _ in range(m + 1)],
            *[rho_3 / k for _ in range(m)]
        ]
        state_probabilities_1 = calculate_probabilities(traffic_intensities_1)
        self.average_lamb = finite_average_lamb()
        self.qs_1 = FiniteStateModelQS(
            state_probabilities=state_probabilities_1,
            arrival_rate=self.average_lamb,
            channel_count=k, queue_length=2 * m + 1, source_limit=None
        )

        self.qs_2 = InfiniteQueueQS(
            lamb=lamb_1, mu=mu_1, k=k
        )
        self.qs_2_lamb = lamb_1
        print(f"mu_1 = {mu_1}")
        print(f"rho_1 = {rho_1}")
        print(f"rho_2 = {rho_2}")
        print(f"rho_3 = {rho_3}")

    def solve(self):
        print(f"Среднее число машин в очереди: {self.qs_1.queue_loading()} | {self.qs_2.n_o()}")
        print(f"Среднее число занятых колонок: {self.qs_1.channels_loading()} | {self.qs_2.k3()}")
        print(f"Средняя интенсивность прибытия машин: {self.average_lamb}")
        print(
            f"Среднее время ожидания машин в очереди: {self.qs_1.queue_average_time()} | {self.qs_2.t_wait()}")


solver = SolverP15B(k=5, a=4, m=5)
solver.solve()
