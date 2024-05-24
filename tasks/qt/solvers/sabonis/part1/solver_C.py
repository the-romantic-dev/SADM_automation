from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
from tasks.qt.models.queueing_systems.impatient_finite_queue_qs import ImpatientFiniteQueueQS
from tasks.qt.models.queueing_systems.model_qs import FiniteStateModelQS
from tasks.qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


class SolverC:
    def __init__(self, n, t1, t2, t3, k, m):
        lamb = n
        mu = 1 / t1
        nu = 1 / t2
        self.lamb = lamb
        self.mu = mu
        self.nu = nu
        self.t1 = t1
        self.t3 = t3
        # self.qs = ImpatientFiniteQueueQS(k=k, m=m, lamb=lamb, mu=mu, nu=nu)
        traffic_intensities = [
            *[lamb / (mu * (j + 1)) for j in range(k)],
            *[lamb / (k * mu + (j + 1) * nu) for j in range(m)]
        ]
        state_probabilities = calculate_probabilities(traffic_intensities)
        self.qs = FiniteStateModelQS(
            state_probabilities=state_probabilities,
            arrival_rate=lamb,
            channel_count=k,
            queue_length=m,
            source_limit=None
        )

    def solve(self):
        print(f"lamb = {self.lamb}")
        print(f"mu = {self.mu}")
        print(f"nu = {self.nu}")
        print(f"rho = {self.lamb / self.mu}")
        print(
            f"t_cт = {self.t1 + self.t3 + self.qs.queue_average_time()}")
        print(f"kз = {self.qs.channels_loading()}")
        print(f"n_o = {self.qs.queue_loading()}")
        escape_probability = self.qs.queue_loading() * self.nu / self.lamb
        refuse_probability = self.qs.state_probability(-1)
        print(f"P_отк = {refuse_probability}")
        print(f"P_ух = {escape_probability}")
        print(
            f"P_об = {1 - escape_probability - refuse_probability}")


solver = SolverC(n=2, t1=4, t2=10, t3=10, k=3, m=15)
solver.solve()
