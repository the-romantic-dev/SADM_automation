import math

from matplotlib import pyplot as plt

from tasks.qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS


class SolverT17658B:
    def __init__(self, a: int, b: int, c: int, d: int, p: float):
        self.lamb = a + b + c
        self.mu = 1 / (d / 60)
        self.p = p
        self.P0 = lambda k: InfiniteQueueQS(k=k, lamb=self.lamb, mu=self.mu).P0()
        print(self.lamb / self.mu)

    def solve(self):
        k_values = list(range(math.ceil(self.lamb / self.mu), 12))
        f_values = [self.P0(k) for k in k_values]
        result_k = 0
        result_f = 0
        pre_result_k = 0
        pre_result_f = 0
        for i in range(len(k_values)):
            if f_values[i] >= self.p:
                result_k = k_values[i]
                result_f = f_values[i]
                pre_result_k = k_values[i - 1]
                pre_result_f = f_values[i - 1]
                break
        print(f"result_k = {result_k}")
        print(f"result_f = {result_f}")
        print(f"pre_result_k = {pre_result_k}")
        print(f"pre_result_f = {pre_result_f}")
        plt.plot(k_values, f_values, label="f")
        plt.plot(k_values, [self.p for _ in k_values], label=f"P={self.p}")

        plt.xlabel('L')
        plt.ylabel('f')
        plt.legend()
        plt.grid(True)
        plt.show()

    # def p_0(self):
    #     result = 1
    #     k = self.k
    #     rho = self.lamb / self.mu
    #     for j in range(1, k + 1):
    #         result += rho ** j / math.factorial(j)
    #     result += rho ** (k + 1) / (math.factorial(k) * (k - rho))
    #     return result ** -1
    #
    # def p_j(self, j):
    #     rho = self.lamb / self.mu
    #     k = self.k
    #     if j <= k:
    #         return rho ** j / math.factorial(j) * self.p_0()
    #     else:
    #         return rho ** j / (math.factorial(k) * k ** (j - k)) * self.p_0()
    #
    # def f(self, l):
    #     result = 0
    #     for j in range(l + self.k + 1):
    #         result += self.p_j(j)
    #     return result


solver = SolverT17658B(a=9, b=9, c=7, d=6, p=0.02)
solver.solve()
