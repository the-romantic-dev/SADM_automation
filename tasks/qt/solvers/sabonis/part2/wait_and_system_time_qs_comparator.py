import enum

import numpy as np
import sympy as sp
from matplotlib import pyplot as plt


class PlotType(enum.Enum):
    WAIT = 1
    SYSTEM = 2


def build_plot(rho_values, f_values, plot_name):
    plt.plot(rho_values, f_values, label="φ(ρ)")
    plt.plot(rho_values, [1 for _ in rho_values], label="φ = 1")
    plt.xlabel('ρ')
    plt.ylabel('φ')
    plt.title(plot_name)
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.clf()
    plt.cla()


class WaitAndSystemTimeQSComparator:
    def __init__(self, qs1, qs2, max_rho_1, max_rho_2):
        self.qs_1 = qs1
        self.qs_2 = qs2
        self.max_rho_1 = max_rho_1
        self.max_rho_2 = max_rho_2

    def solve(self):
        max_rho_1 = self.max_rho_1
        max_rho_2 = self.max_rho_2
        rho_1_values, f1_values = self.build_values(plot_type=PlotType.WAIT, max_rho=max_rho_1 - 0.01, steps=100)
        rho_2_values, f2_values = self.build_values(plot_type=PlotType.SYSTEM, max_rho=max_rho_2 - 0.01, steps=200)

        build_plot(rho_1_values, f1_values, plot_name="Время ожидания")
        build_plot(rho_2_values, f2_values, plot_name="Время в системе")

    def build_values(self, plot_type: PlotType, max_rho, steps):
        lamb = sp.symbols("λ")
        mu = sp.symbols("μ")
        if plot_type == PlotType.WAIT:
            if self.qs_2.t_wait() != 0:
                f = self.qs_1.t_wait() / self.qs_2.t_wait()
            else:
                f = 0
        else:
            f = self.qs_1.t_sys() / self.qs_2.t_sys()

        rho_values = np.linspace(0.1, max_rho, steps)
        if f == 0:
            f_values = [0 for _ in rho_values]
        else:
            f_values = [f.subs(lamb, rho).subs(mu, 1) for rho in rho_values]
        return rho_values, f_values
