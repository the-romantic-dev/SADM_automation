import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def p_0(k, m, rho):
    if isinstance(m, str):
        s1 = sum([rho ** j / math.factorial(j) for j in range(1, k + 1)])
        s2 = rho ** (k + 1) / (math.factorial(k) * (k - rho))
        return (1 + s1 + s2) ** -1
    else:
        s1 = sum([rho ** j / math.factorial(j) for j in range(1, k + 1)])
        s2 = rho ** (k + 1) * (1 - (1 / k * rho) ** m) / (math.factorial(k) * k * (1 - 1 / k * rho))
        return (1 + s1 + s2) ** -1


def p_err(k, m, rho):
    return rho ** (k + m) * p_0(k, m, rho) / (math.factorial(k) * k ** m)


def n_o(k, m, rho):
    if isinstance(m, str):
        return rho ** (k + 1) * p_0(k, m, rho) / (math.factorial(k) * k * (1 - 1 / k * rho) ** 2)
    elif m > 0:
        factor = rho ** (k + 1) * p_0(k, m, rho)
        top = 1 - (1 / k * rho) ** m * (m + 1 - 1 / k * m * rho)
        bottom = (math.factorial(k) * k * (1 - 1 / k * rho) ** 2)
        return factor * (top / bottom)
    else:
        return 0


def p(a, b, c):
    return a + b + c - a * b - b * c - a * c + a * b * c


class Solver81:
    def __init__(self, k: int, m: str | int):
        self.k = k
        self.m = m

    def phi_ozh(self):
        m = self.m
        if m == 0:
            return 0
        k = self.k
        rho = sp.symbols("ρ")
        rho_1 = rho
        rho_2 = k * rho
        return k * (n_o(1, m, rho_1) + n_o(2, m, rho_1) + n_o(k, m, rho_1)) / (3 * n_o(k + 3, k * m, rho_2))

    def phi_c(self):
        m = self.m
        k = self.k
        rho = sp.symbols("ρ")
        rho_1 = rho
        rho_2 = k * rho
        no1 = (n_o(1, m, rho_1) + n_o(2, m, rho_1) + n_o(k, m, rho_1)) / 3
        no2 = n_o(k + 3, k * m, rho_2)
        if isinstance(m, str):
            return (no1 + rho_1) / (no2 + rho_2)
        else:
            p_err_1 = p(p_err(1, m, rho_1), p_err(2, m, rho_1), p_err(k, m, rho_1))
            p_err_2 = p_err(k + 3, k * m, rho_2)
            if m > 0:
                return (no1 + rho_1 * (1 - p_err_1)) / (no2 + rho_2 * (1 - p_err_2))
            else:
                return (1 - p_err_1) / (1 - p_err_2)

    def solve(self):
        phi_1 = self.phi_ozh()
        phi_2 = self.phi_c()
        rho = sp.symbols("ρ")

        steps = 100
        rho_values = np.linspace(0.01, 1, steps)
        if phi_1 != 0:
            phi_1_values = [phi_1.subs(rho, rho_val) for rho_val in rho_values]
        else:
            phi_1_values = [0 for _ in rho_values]
        phi_2_values = [phi_2.subs(rho, rho_val) for rho_val in rho_values]

        phi_1_eq_value = None
        phi_2_eq_value = None
        for i in range(len(rho_values)):
            try:
                if phi_1_values[i] < 1:
                    phi_1_eq_value = rho_values[i]
                    break
            except TypeError:
                continue

        for i in range(len(rho_values)):
            try:
                if phi_2_values[i] < 1:
                    phi_2_eq_value = rho_values[i]
                    break
            except TypeError:
                continue

        print(f"φ_1 = 1 при rho = {phi_1_eq_value}")
        print(f"φ_2 = 1 при rho = {phi_2_eq_value}")
        print(f"φ_1_last = {phi_1_values[-1]}")
        print(f"φ_2_last = {phi_2_values[-1]}")
        # Строим график
        plt.plot(rho_values, phi_1_values)
        plt.xlabel('ρ')
        plt.ylabel('φ')
        plt.title('φ_ож')
        plt.grid(True)
        plt.show()

        plt.clf()
        plt.cla()

        plt.plot(rho_values, phi_2_values)
        plt.xlabel('ρ')
        plt.ylabel('φ')
        plt.title('φ_с')
        plt.grid(True)
        plt.show()


solver = Solver81(k=2, m=1)
solver.solve()
