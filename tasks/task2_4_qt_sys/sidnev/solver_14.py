import math
from enum import Enum

import numpy as np
import sympy as sp
from sympy import Eq, solve


class NodeType(Enum):
    FIFO = 1
    IS = 2

def generate_probabilities_indices(n, length, current_sum=0, current_index=[], result=[]):
    if length == 0:
        if current_sum == n:
            result.append(tuple(current_index))
        return

    for num in range(n - current_sum + 1):
        generate_probabilities_indices(n, length - 1, current_sum + num, [*current_index, num], result)

    return result

def build_transition_matrix():
    result = np.zeros([M, M], float)
    result[0][1] = 1
    result[1][2] = 1
    for j in range(L):
        result[2][3 + j] = 1 / L
        result[3 + j][21 + j] = fail_prob
        result[3 + j][39 + j] = 1 - fail_prob
        result[21 + j][3 + j] = 1
        result[39 + j][0] = 1
    return result


def get_node_type(i):
    if i in [0, 2] or i in range(3, 20 + 1):
        return NodeType.FIFO
    else:
        return NodeType.IS


def get_mu(i):
    if i == 0:
        return lamb_01, lamb_02
    elif i == 1:
        return mu_per_1, mu_per_2
    elif i == 2:
        return mu_pr, mu_pr
    elif i in range(3, 21):
        return mu_per_1, mu_per_2
    elif i in range(21, 39):
        return 0.5 * mu_per_1, 0.5 * mu_per_2
    elif i in range(39, 57):
        return 10 * mu_per_1, 10 * mu_per_2


def Z(i: int, ni: tuple):
    mu_1, mu_2 = get_mu(i)

    result = omegas_values[omegas[i]] ** (sum(ni))
    result /= math.factorial(ni[0]) * math.factorial(ni[1]) * mu_1 ** ni[0] * mu_2 ** ni[1]

    if get_node_type(i) == NodeType.FIFO:
        result *= math.factorial(sum(ni))
    return result


lamb_01 = 7
lamb_02 = 8
N1 = 15
N2 = 25
L = 18
mu_per_1 = 0.5
mu_per_2 = 1
mu_pr = 10
fail_prob = 0.1
M = 57

transition_matrix = build_transition_matrix()

omegas = sp.symbols(" ".join([f"ω{i}" for i in range(M)]))

equations = []
for j in range(M):
    equations.append(
        Eq(omegas[j], sum([omegas[i] * transition_matrix[i][j] for i in range(M)]))
    )
equations.append(
    Eq(sum(omegas), 1)
)
omegas_values = solve(equations, dict=True)[0]
# for omega in omegas:
#     print(f"{omega} = {omegas_values[omega]}")
n1vars = generate_probabilities_indices(N1, M)
print(n1vars)