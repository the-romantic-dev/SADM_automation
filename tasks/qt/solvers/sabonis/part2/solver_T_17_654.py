import math

import numpy as np
from matplotlib import pyplot as plt


class SolverT17654:
    def __init__(self, a: int, b: int):
        self.lamb = a / 3600
        self.b = b
        self.mu = 1 / 300

    def solve(self):
        f = self.t_ozh

        min_k = int(self.lamb / self.mu) + 1
        max_k = min_k + 5
        k_values = list(range(min_k, max_k))
        f_values = [f(k) for k in k_values]
        result_k = 0
        result_f = 0
        pre_result_k = 0
        pre_result_f = 0
        for i in range(len(k_values)):
            if f_values[i] <= self.b:
                result_k = k_values[i]
                result_f = f_values[i]
                pre_result_k = k_values[i-1]
                pre_result_f = f_values[i-1]
                break
        print(f"result_k = {result_k}")
        print(f"result_f = {result_f}")
        print(f"pre_result_k = {pre_result_k}")
        print(f"pre_result_f = {pre_result_f}")
        plt.plot(k_values, f_values, label="t_ож")
        plt.plot(k_values, [self.b for _ in k_values], label="b")

        plt.xlabel('k')
        plt.ylabel('t')
        plt.legend()
        plt.grid(True)
        plt.show()

    def t_ozh(self, k):
        return self.n_o(k) / self.lamb

    def n_o(self, k):
        rho = self.lamb / self.mu
        rho_c = rho / k
        return rho ** (k + 1) * self.p_0(k) / (k * (1 - rho_c) ** 2 * math.factorial(k))

    def p_0(self, k):
        result = 1
        rho = self.lamb / self.mu
        for j in range(1, k + 1):
            result += rho ** j / math.factorial(j)
        result += rho ** (k + 1) / (math.factorial(k) * (k - rho))
        return result ** -1


solver = SolverT17654(a=60, b=40)
solver.solve()
