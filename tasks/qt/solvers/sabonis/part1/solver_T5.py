from tasks.qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.qt.models.queueing_systems.probabilities_calculator import calculate_probabilities

class SolverT5:
    def __init__(self, lamb, t, k, m, n):
        lamb = lamb
        mu = 1 / (t / 60)
        traffic_intensities_1 = [
            *[lamb / (mu * (j + 1)) for j in range(k)],
            *[lamb / (k * mu) for _ in range(m - k + 1)],
            *[(lamb - 1) / (k * mu) for _ in range(n - m - 1)]
        ]
        state_probabilities_1 = calculate_probabilities(traffic_intensities_1)
        traffic_intensities_2 = [
            *[lamb / (mu * (j + 1)) for j in range(k)],
            *[lamb / (k * mu) for _ in range(n - k)]
        ]
        state_probabilities_2 = calculate_probabilities(traffic_intensities_2)
        self.k = k
        self.qs_1 = FiniteStateModelQS(
            state_probabilities=state_probabilities_1,
            arrival_rate=lamb,
            channel_count=k,
            queue_length=n - k,
            source_limit=None
        )
        self.qs_2 = FiniteStateModelQS(
            state_probabilities=state_probabilities_2,
            arrival_rate=lamb,
            channel_count=k,
            queue_length=n - k,
            source_limit=None
        )

    def solve(self):
        print(f"P_отк = {(self.qs_1.state_probability(-1))} | {self.qs_2.state_probability(-1)}")
        p_z = lambda qs: 1 - sum([qs.state_probability(i) for i in range(self.k)])
        print(f"P_з = {p_z(self.qs_1)} | {p_z(self.qs_2)}")
        print(f"kз = {self.qs_1.channels_loading()} | {self.qs_2.channels_loading()}")
        print(f"n_o = {self.qs_1.queue_loading()} | {self.qs_2.queue_loading()}")


solver = SolverT5(lamb=5, t=40, k=4, m=5, n=10)
solver.solve()
