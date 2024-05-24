from tasks.qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


def active_channels_count(j, k, l):
    if j == 0:
        return 0
    return min(k, divmod(j - 1, l)[0] + 1)


def queue_count(probabilities, k, l):
    result = []
    for j in range(1, len(probabilities)):
        channels_count = active_channels_count(j, k, l)
        result.append(probabilities[j] * (j - channels_count))
    return sum(result)


class SolverA17B:
    def __init__(self, lamb, k, l, t, m):
        lamb = lamb
        mu = 1 / (t / 60)
        self.k = k
        self.m = m
        self.rho = lamb / mu
        self.l = l
        traffic_intensities = [
            *[lamb / (active_channels_count(j + 1, k, l) * mu) for j in range(m + k)]
        ]
        self.state_probabilities = calculate_probabilities(traffic_intensities)

    def solve(self):
        print(f"n_o = {queue_count(self.state_probabilities, self.k, self.l)}")
        print(f"P_отк = {self.state_probabilities[-1]}")


solver = SolverA17B(lamb=5, k=2, l=3, t=20, m=12)
solver.solve()
