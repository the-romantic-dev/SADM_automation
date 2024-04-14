import math

import numpy as np
from matplotlib import pyplot as plt


class SolverT17655:
    def __init__(self, k: int, b: int, p: float):
        self.lamb = 1 / 3
        self.mu = 1 / b
        self.k = k
        self.p = p

    def solve(self):
        f = self.f

        l_values = list(range(0, 12))
        f_values = [f(l) for l in l_values]
        result_l = 0
        result_f = 0
        pre_result_l = 0
        pre_result_f = 0
        for i in range(len(l_values)):
            if f_values[i] >= self.p:
                result_l = l_values[i]
                result_f = f_values[i]
                pre_result_l = l_values[i - 1]
                pre_result_f = f_values[i - 1]
                break
        print(f"result_l = {result_l}")
        print(f"result_f = {result_f}")
        print(f"pre_result_l = {pre_result_l}")
        print(f"pre_result_f = {pre_result_f}")
        plt.plot(l_values, f_values, label="f")
        plt.plot(l_values, [self.p for _ in l_values], label=f"P={self.p}")

        plt.xlabel('L')
        plt.ylabel('f')
        plt.legend()
        plt.grid(True)
        plt.show()

    def p_0(self):
        result = 1
        k = self.k
        rho = self.lamb / self.mu
        for j in range(1, k + 1):
            result += rho ** j / math.factorial(j)
        result += rho ** (k + 1) / (math.factorial(k) * (k - rho))
        return result ** -1

    def p_j(self, j):
        rho = self.lamb / self.mu
        k = self.k
        if j <= k:
            return rho ** j / math.factorial(j) * self.p_0()
        else:
            return rho ** j / (math.factorial(k) * k ** (j - k)) * self.p_0()

    def f(self, l):
        result = 0
        for j in range(l + self.k + 1):
            result += self.p_j(j)
        return result


solver = SolverT17655(k=4, b=7, p=0.999)
solver.solve()
