# Сиднев модель с интенсивностями
import numpy as np
from scipy.optimize import minimize

all_edges = [
    (1, 2, 5), (1, 3, 4), (1, 4, 4), (1, 5, 7),
    (2, 6, 6),
    (3, 6, 7),
    (4, 5, 6), (4, 7, 5),
    (5, 6, 5), (5, 7, 5), (5, 8, 4),
    (6, 7, 5), (6, 8, 5),
    (7, 8, 3),
    (8, 9, 7),
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
    nodes = set([edge[0] for edge in all_edges] + [edge[1] for edge in all_edges])
    in_edges = lambda node: [edge for edge in all_edges if edge[1] == node]
    out_edges = lambda node: [edge for edge in all_edges if edge[0] == node]
    result = [
        0.75 * len(all_edges) - sum(m_variables)
    ]
    for node in nodes:
        for out_edge in out_edges(node):
            for in_edge in in_edges(node):
                result.append(
                    tau(out_edge[0], out_edge[1]) - tau(in_edge[0], in_edge[1]) - in_edge[2] / m(in_edge[0], in_edge[1])
                )
    for in_edge in in_edges(max(nodes)):
        result.append(T - tau(in_edge[0], in_edge[1]) - in_edge[2] / m(in_edge[0], in_edge[1]))
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
