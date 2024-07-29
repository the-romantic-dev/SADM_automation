import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, simplify

from tasks.task2_3_qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS

beta_range = np.linspace(0.1, 0.9, 100)


def replace_beta(model: InfiniteQueueQS, function, rho_beta):
    _lamb, rho = symbols("λ ρ")
    lamb = model.lamb
    mu = model.mu
    function_rho = simplify(function.subs(_lamb, rho * mu * _lamb / lamb))
    function_beta = function_rho.subs(rho, rho_beta)
    return simplify(function_beta)


class Solver8:
    def __init__(self, k, m):
        self.k = k
        self.m = m

        lamb, mu = symbols("λ μ")
        self.model_a = InfiniteQueueQS(k=1, lamb=lamb, mu=mu)
        self.model_b = InfiniteQueueQS(k=k, lamb=k * lamb, mu=mu)
        self.model_c = InfiniteQueueQS(k=1, lamb=k * lamb, mu=k * mu)

    def plot_t_wait(self):
        beta = symbols("β")
        t_wait_a = replace_beta(self.model_a, self.model_a.t_wait(), beta)
        t_wait_b = replace_beta(self.model_b, self.model_b.t_wait(), self.k * beta)
        t_wait_c = replace_beta(self.model_c, self.model_c.t_wait(), beta)
        ab_values = [(t_wait_a / t_wait_b).subs(beta, i) for i in beta_range]
        bc_values = [(t_wait_b / t_wait_c).subs(beta, i) for i in beta_range]
        ca_values = [(t_wait_c / t_wait_a).subs(beta, i) for i in beta_range]
        plt.plot(beta_range, ab_values, label="Отношение t_ож_a / t_ож_б")
        plt.plot(beta_range, bc_values, label="Отношение t_ож_б / t_ож_в")
        plt.plot(beta_range, ca_values, label="Отношение t_ож_в / t_ож_а")
        plt.xlabel("β")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_t_sys(self):
        beta = symbols("β")
        t_sys_a = replace_beta(self.model_a, self.model_a.t_sys(), beta)
        t_sys_b = replace_beta(self.model_b, self.model_b.t_sys(), self.k * beta)
        t_sys_c = replace_beta(self.model_c, self.model_c.t_sys(), beta)
        ab_values = [(t_sys_a / t_sys_b).subs(beta, i) for i in beta_range]
        bc_values = [(t_sys_b / t_sys_c).subs(beta, i) for i in beta_range]
        ca_values = [(t_sys_c / t_sys_a).subs(beta, i) for i in beta_range]
        plt.plot(beta_range, ab_values, label="Отношение t_c_a / t_c_б")
        plt.plot(beta_range, bc_values, label="Отношение t_c_б / t_c_в")
        plt.plot(beta_range, ca_values, label="Отношение t_c_в / t_c_а")
        plt.xlabel("β")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_n_o(self):
        beta = symbols("β")
        n_o_a = replace_beta(self.model_a, self.model_a.n_o(), beta)
        n_o_b = replace_beta(self.model_b, self.model_b.n_o(), self.k * beta)
        n_o_c = replace_beta(self.model_c, self.model_c.n_o(), beta)
        a_values = [n_o_a.subs(beta, i) for i in beta_range]
        b_values = [n_o_b.subs(beta, i) for i in beta_range]
        c_values = [n_o_c.subs(beta, i) for i in beta_range]
        plt.plot(beta_range, a_values, label="n_o_a и n_o_в")
        plt.plot(beta_range, b_values, label="n_o_б")
        # plt.plot(beta_range, c_values, label="n_o_в")
        plt.xlabel("β")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_k_3(self):
        beta = symbols("β")
        k_3_a = replace_beta(self.model_a, self.model_a.k3(), beta)
        k_3_b = replace_beta(self.model_b, self.model_b.k3(), self.k * beta)
        k_3_c = replace_beta(self.model_c, self.model_c.k3(), beta)
        a_values = [k_3_a.subs(beta, i) for i in beta_range]
        b_values = [k_3_b.subs(beta, i) for i in beta_range]
        c_values = [k_3_c.subs(beta, i) for i in beta_range]
        plt.plot(beta_range, a_values, label="k_з_a и k_з_в")
        plt.plot(beta_range, b_values, label="k_з_б")
        # plt.plot(beta_range, c_values, label="n_o_в")
        plt.xlabel("β")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_j(self):
        beta = symbols("β")
        j_a = replace_beta(self.model_a, self.model_a.j(), beta)
        j_b = replace_beta(self.model_b, self.model_b.j(), self.k * beta)
        j_c = replace_beta(self.model_c, self.model_c.j(), beta)
        a_values = [j_a.subs(beta, i) for i in beta_range]
        b_values = [j_b.subs(beta, i) for i in beta_range]
        c_values = [j_c.subs(beta, i) for i in beta_range]
        plt.plot(beta_range, a_values, label="j_a и j_в")
        plt.plot(beta_range, b_values, label="j_б")
        # plt.plot(beta_range, c_values, label="n_o_в")
        plt.xlabel("β")
        plt.legend()
        plt.grid()
        plt.show()


solver = Solver8(k=2, m=None)
# solver.plot_t_wait()
# solver.plot_t_sys()
# solver.plot_n_o()
solver.plot_j()
