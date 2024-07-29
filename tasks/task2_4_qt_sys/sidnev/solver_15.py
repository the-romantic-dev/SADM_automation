from dataclasses import dataclass

import numpy as np
from sympy import symbols, linear_eq_to_matrix


@dataclass
class QTData:
    nodes: int
    requests: int
    matrix: list[list[float]]
    mu: list[int]
    channels: list[int]


def calculate_omegas(data_index: int):
    _data = data[data_index]
    _omegas = symbols(" ".join([f"ω{i}" for i in range(_data.nodes)]))
    equations = []
    for j in range(_data.nodes):
        equations.append(
            _omegas[j] - sum([_omegas[i] * _data.matrix[i][j] for i in range(_data.nodes)])
        )
    equations.append(
        sum(_omegas) - 1
    )

    A, b = linear_eq_to_matrix(equations, _omegas)
    A_np = np.array(A.tolist(), dtype="float")
    b_np = np.array(b.tolist(), dtype="float")
    solution = np.linalg.lstsq(A_np, b_np, rcond=None)
    result = list(solution[0].transpose()[0])

    return result


def lamb_1(r, data_index: int):
    if calculated_lamb_1[data_index][r - 1] != -1:
        return calculated_lamb_1[data_index][r - 1]
    _data = data[data_index]
    result = r
    result /= sum([omegas[data_index][j] / omegas[data_index][0] * t(j, r, data_index) for j in range(_data.nodes)])
    calculated_lamb_1[data_index][r - 1] = result
    return result


def P(i, n, r, data_index: int):
    if calculated_P[data_index][i][r - 1][n] != -1:
        return calculated_P[data_index][i][r - 1][n]
    if n == 0 and r == 0:
        result = 1
    elif n == 0:
        result = 1 - sum([P(i, _n + 1, r, data_index) for _n in range(r)])
    else:
        result = omegas[data_index][i] * lamb_1(r, data_index)
        result /= omegas[data_index][0] * mu(i, n, data_index)
        result *= P(i, n - 1, r - 1, data_index)
    calculated_P[data_index][i][r - 1][n] = result
    return result


def mu(i, n, data_index: int):
    _data = data[data_index]
    return _data.mu[i] * min(n, _data.channels[i])


def t(i: int, r, data_index: int):
    _data = data[data_index]
    summers = []
    for n in range(r):
        s1 = n + 1
        s2 = mu(i, n + 1, data_index)
        s3 = P(i, n, r - 1, data_index)
        s = s1 / s2 * s3
        summers.append(s)
    result = sum(summers)
    return result


def n(i, r, data_index):
    result = omegas[data_index][i] / omegas[data_index][0] * lamb_1(r, data_index) * t(i, r, data_index)
    return result


def load_factor(i, data_index):
    return node_requests[data_index][i] / node_times[data_index][i] / data[data_index].mu[i]


def node_prob(i, data_index):
    result = omegas[data_index][i] * node_times[data_index][i]
    result /= sum([omegas[data_index][j] * node_times[data_index][j] for j in range(data[data_index].nodes)])
    return result


def queue_t(i, data_index):
    return node_times[data_index][i] - 1 / data[data_index].mu[i]


def n_queue(i, data_index):
    return node_requests[data_index][i] * node_queue_times[data_index][i] / node_times[data_index][i]


data = [
    QTData(
        nodes=4, requests=3, mu=[3, 1, 7, 9], channels=[1, 2, 1, 1],
        matrix=[
            [0.3636, 0, 0.6364, 0],
            [0, 0, 0.7143, 0.2857],
            [0.25, 0.45, 0, 0.3],
            [1, 0, 0, 0],
        ]
    ),
    QTData(
        nodes=4, requests=4, mu=[8, 9, 8, 1], channels=[2, 2, 2, 3],
        matrix=[
            [0.125, 0.625, 0.0625, 0.1875],
            [0.4, 0, 0.6, 0],
            [0.7692, 0.1538, 0, 0.0769],
            [0, 0.5833, 0.4167, 0],
        ]
    ),
    QTData(
        nodes=7, requests=15, mu=[2, 7, 10, 2, 4, 10, 6], channels=[3, 3, 2, 3, 1, 1, 2],
        matrix=[
            [0.2632, 0, 0.2105, 0.4211, 0, 0.1053, 0],
            [0.0294, 0, 0.1471, 0.2941, 0.0882, 0.2647, 0.1765],
            [0.3125, 0, 0, 0.0938, 0.0625, 0.3125, 0.2188],
            [0, 0.4737, 0.4211, 0, 0, 0, 0.1053],
            [0, 0.2222, 0.2778, 0.2778, 0, 0, 0.2222],
            [0.1707, 0.0976, 0.1707, 0.1463, 0.1707, 0, 0.2439],
            [0.6923, 0, 0, 0.0769, 0, 0.2308, 0]
        ]
    ),
    QTData(
        nodes=7, requests=16, mu=[7, 10, 6, 10, 4, 7, 4], channels=[3, 2, 3, 2, 1, 1, 3],
        matrix=[
            [0.0435, 0, 0.0435, 0.3478, 0.1304, 0, 0.4348],
            [0.2963, 0, 0, 0.3704, 0.3333, 0, 0],
            [0.1290, 0.3226, 0, 0.0968, 0.0968, 0.2903, 0.0645],
            [0.2308, 0.3846, 0.3846, 0, 0, 0, 0],
            [0.1176, 0.2941, 0.2059, 0.0882, 0, 0.0882, 0.2059],
            [0, 0.3182, 0.0909, 0, 0.3636, 0, 0.2273],
            [0, 0, 0, 0, 0, 1, 0]
        ]
    ),

]

# Кэширование данных при вычислениях
calculated_lamb_1 = [[-1 for _ in range(d.requests)] for d in data]
calculated_P = [[[[-1 for _ in range(r + 2)] for r in range(d.requests)] for _ in range(d.nodes)] for d in data]

# Вероятности посещения узлов
omegas = [calculate_omegas(di) for di in range(len(data))]

# Параметры систем
node_times = [[t(i, d.requests, data_index=di) for i in range(d.nodes)] for di, d in enumerate(data)]
node_requests = [[n(i, d.requests, data_index=di) for i in range(d.nodes)] for di, d in enumerate(data)]
load_factors = [[load_factor(i, di) for i in range(d.nodes)] for di, d in enumerate(data)]
node_probabilities = [[node_prob(i, di) for i in range(d.nodes)] for di, d in enumerate(data)]
node_queue_times = [[queue_t(i, di) for i in range(d.nodes)] for di, d in enumerate(data)]
node_queue_requests = [[n_queue(i, di) for i in range(d.nodes)] for di, d in enumerate(data)]


def show_properties(properties):
    return ' | '.join([f'{round(prop, 4)}' for prop in properties])


for system_index, _ in enumerate(data):
    print(f"Система #{system_index + 1}:")
    print(f"Среднее время в узле: {show_properties(node_times[system_index])}")
    print(f"Среднее число заявок: {show_properties(node_requests[system_index])}")
    print(f"Коэффициент загрузки: {show_properties(load_factors[system_index])}")
    print(f"Вероятность пребывания узле: {show_properties(node_probabilities[system_index])}")
    print(f"Среднее время в очереди: {show_properties(node_queue_times[system_index])}")
    print(f"Среднее число заявок в очереди: {show_properties(node_queue_requests[system_index])}")
