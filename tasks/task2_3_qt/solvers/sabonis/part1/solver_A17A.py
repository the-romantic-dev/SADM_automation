from tasks.task2_3_qt.models.queueing_systems.probabilities_calculator import calculate_probabilities


def active_channels_count(j, k, l):
    # if j <= l + 1:
    #     return 1
    return min(k, max(j - l, 1))


def queue_count(probabilities, k, l):
    result = []
    for j in range(1, len(probabilities)):
        channels_count = active_channels_count(j, k, l)
        result.append(probabilities[j] * (j - channels_count))
    return sum(result)


class SolverA17A:
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


solver = SolverA17A(lamb=10, k=3, l=3, t=12, m=12)
solver.solve()
