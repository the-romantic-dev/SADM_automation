# Сиднев модель с интенсивностями
import numpy as np
from scipy.optimize import minimize

all_edges = [
    (1, 2, 7), (1, 3, 7), (1, 5, 4),
    (2, 4, 7), (2, 5, 4),
    (3, 5, 5),
    (4, 7, 5),
    (5, 6, 7), (5, 7, 4),
    (6, 7, 7), (6, 8, 6), (6, 9, 7),
    (7, 8, 7), (7, 9, 3),
    (8, 9, 3)
]
max_i = 10
linear_indices = [edge[0] * max_i + edge[1] for edge in all_edges]


def linear_index(i, j):
    return linear_indices.index(i * max_i + j)


def get_ij_by_linear_index(index):
    ij = linear_indices[index]
    i = ij // max_i
    j = ij % max_i
    return i, j


def obj(variables):
    tau = variables[len(variables) // 2 + 1:]
    T = variables[len(variables) // 2]
    return sum(tau) + T


def constraints(variables):
    def tau(i, j):
        l_index = linear_index(i, j)
        return tau_variables[l_index]

    def m(i, j):
        l_index = linear_index(i, j)
        return m_variables[l_index]

    m_variables = variables[:len(variables) // 2]
    tau_variables = variables[len(variables) // 2 + 1:]
    T = variables[len(variables) // 2]
    result = [
        0.75 * len(all_edges) - sum(m_variables),
        tau(2, 5) - tau(1, 2) - 7 / m(1, 2),
        tau(2, 4) - tau(1, 2) - 7 / m(1, 2),
        tau(3, 5) - tau(1, 3) - 7 / m(1, 3),
        tau(4, 7) - tau(2, 4) - 7 / m(2, 4),
        tau(5, 7) - tau(1, 5) - 4 / m(1, 5),
        tau(5, 7) - tau(2, 5) - 4 / m(2, 5),
        tau(5, 7) - tau(3, 5) - 5 / m(3, 5),
        tau(5, 6) - tau(1, 5) - 4 / m(1, 5),
        tau(5, 6) - tau(2, 5) - 4 / m(2, 5),
        tau(5, 6) - tau(3, 5) - 5 / m(3, 5),
        tau(6, 7) - tau(5, 6) - 7 / m(5, 6),
        tau(6, 8) - tau(5, 6) - 7 / m(5, 6),
        tau(6, 9) - tau(5, 6) - 7 / m(5, 6),
        tau(7, 8) - tau(5, 7) - 4 / m(5, 7),
        tau(7, 8) - tau(4, 7) - 5 / m(4, 7),
        tau(7, 8) - tau(6, 7) - 7 / m(6, 7),
        tau(7, 9) - tau(5, 7) - 4 / m(5, 7),
        tau(7, 9) - tau(4, 7) - 5 / m(4, 7),
        tau(7, 9) - tau(6, 7) - 7 / m(6, 7),
        tau(8, 9) - tau(7, 8) - 7 / m(7, 8),
        tau(8, 9) - tau(6, 8) - 6 / m(6, 8),
        T - tau(7, 9) - 3 / m(7, 9),
        T - tau(6, 9) - 7 / m(6, 9),
        T - tau(8, 9) - 3 / m(8, 9),
    ]
    return result


def solve_intensive_model():
    initial_guess = np.ones(len(all_edges) * 2 + 1)
    bounds = [(0, None)] * len(initial_guess)
    solution = minimize(
        fun=obj,
        x0=initial_guess,
        constraints={'type': 'ineq', 'fun': constraints},
        bounds=bounds)
    t_result = {}
    m_result = {}
    for index in range(len(all_edges)):
        i, j = get_ij_by_linear_index(index)
        m_value = round(solution.x[:len(solution.x) // 2][index], 4)
        t_value = round(solution.x[len(solution.x) // 2 + 1:][index], 4)
        m_result[(i, j)] = m_value
        t_result[(i, j)] = t_value
    T_result = round(solution.x[len(solution.x) // 2], 4)
    return t_result, m_result, T_result

print(solve_intensive_model())