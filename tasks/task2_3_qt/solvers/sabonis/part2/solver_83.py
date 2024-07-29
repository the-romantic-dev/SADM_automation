from tasks.task2_3_qt.solvers.sabonis.part2.wait_and_system_time_qs_comparator import WaitAndSystemTimeQSComparator

import enum

import numpy as np
from matplotlib import pyplot as plt

from tasks.task2_3_qt.models.queueing_systems.finite_queue_qs import FiniteQueueQS
import sympy as sp

from tasks.task2_3_qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS


class PlotType(enum.Enum):
    WAIT = 1
    SYSTEM = 2

def find_equality_1_rho(rho_values, f_values):
    for i in range(1, len(f_values)):
        if f_values[i - 1] < 1 and f_values[i] > 1:
            return rho_values[i]
        if f_values[i - 1] > 1 and f_values[i] < 1:
            return rho_values[i]
    return None

def build_plot(rho_values, f_values, plot_name):
    plt.plot(rho_values, f_values, label="φ(ρ)")
    plt.plot(rho_values, [1 for _ in rho_values], label="φ=1")
    plt.xlabel('ρ')
    plt.ylabel('φ')
    plt.title(plot_name)
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.clf()
    plt.cla()


class Solver83:
    def __init__(self, k):
        lamb = sp.symbols("λ")
        mu = sp.symbols("μ")
        self.k = k
        self.qs_1 = InfiniteQueueQS(k=k, lamb=lamb, mu=mu)
        self.qs_2 = InfiniteQueueQS(k=k, lamb=lamb, mu=2 * mu)

    def solve(self):
        max_rho = self.k
        rho_1_values, f1_values = self.build_values(plot_type=PlotType.WAIT, max_rho=max_rho - 0.01, steps=100)
        rho_2_values, f2_values = self.build_values(plot_type=PlotType.SYSTEM, max_rho=max_rho - 0.01, steps=100)

        print(f"f1: {find_equality_1_rho(rho_1_values, f1_values)}")
        print(f"f2: {find_equality_1_rho(rho_2_values, f2_values)}")

        build_plot(rho_1_values, f1_values, plot_name="Время ожидания")
        build_plot(rho_2_values, f2_values, plot_name="Время в системе")

    def build_values(self, plot_type: PlotType, max_rho, steps):
        lamb = sp.symbols("λ")
        mu = sp.symbols("μ")
        if plot_type == PlotType.WAIT:
            if self.qs_2.t_wait() != 0:
                f = self.qs_1.t_wait() / (2 * self.qs_2.t_wait())
            else:
                f = 0
        else:
            f = self.qs_1.t_sys() / (2 * self.qs_2.t_sys())

        rho_values = np.linspace(0.01, max_rho, steps)
        if f == 0:
            f_values = [0 for _ in rho_values]
        else:
            f_values = [f.subs(lamb, rho).subs(mu, 1) for rho in rho_values]
        return rho_values, f_values


solver = Solver83(k=2)
solver.solve()
