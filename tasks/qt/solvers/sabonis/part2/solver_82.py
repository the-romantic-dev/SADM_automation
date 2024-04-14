import enum

import numpy as np
from matplotlib import pyplot as plt

from tasks.qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
import sympy as sp

from tasks.qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS


class PlotType(enum.Enum):
    WAIT = 1
    SYSTEM = 2


def build_plot(rho_values, f_values, plot_name):
    plt.plot(rho_values, f_values)
    # plt.plot(rho_values, [1 for _ in rho_values])
    plt.xlabel('ρ')
    plt.ylabel('φ')
    plt.title(plot_name)
    plt.grid(True)
    plt.show()

    plt.clf()
    plt.cla()


class Solver82:
    def __init__(self, k, m):
        lamb = sp.symbols("λ")
        mu = sp.symbols("μ")
        self.k = k
        if isinstance(m, int):
            self.qs_1 = FiniteQueueQS(k=k + 3, m=k * m, lamb=k * lamb, mu=mu)
            self.qs_2 = FiniteQueueQS(k=1, m=k * m, lamb=k * lamb, mu=k * mu)
        else:
            self.qs_1 = InfiniteQueueQS(k=k + 3, lamb=k * lamb, mu=mu)
            self.qs_2 = InfiniteQueueQS(k=1, lamb=k * lamb, mu=k * mu)

    def solve(self):
        max_rho_1 = 1
        max_rho_2 = 1
        rho_1_values, f1_values = self.build_values(plot_type=PlotType.WAIT, max_rho=max_rho_1 - 0.01, steps=100)
        rho_2_values, f2_values = self.build_values(plot_type=PlotType.SYSTEM, max_rho=max_rho_2 - 0.01, steps=200)
        for i in range(1, len(f2_values)):
            if f2_values[i] < 1 < f2_values[i - 1]:
                rho_1 = float(rho_2_values[i - 1])
                rho_2 = float(rho_2_values[i])
                f1 = float(f2_values[i - 1])
                f2 = float(f2_values[i])
                print(f"f({round(rho_1, 4)}) = {round(f1, 4)}")
                print(f"f({round(rho_2, 4)}) = {round(f2, 4)}")
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

        rho_values = np.linspace(0.01, max_rho, steps)
        if f == 0:
            f_values = [0 for _ in rho_values]
        else:
            f_values = [f.subs(lamb, rho).subs(mu, 1) for rho in rho_values]
        return rho_values, f_values


solver = Solver82(k=2, m=2)
solver.solve()
