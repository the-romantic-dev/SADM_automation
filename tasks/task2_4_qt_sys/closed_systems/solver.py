import math
from dataclasses import dataclass

import tasks.task2_4_qt_sys.closed_systems.data as data
from sympy import symbols, Eq, Rational
from sympy.solvers import solve


def calculate_alphas(lambdas):
    return [lambdas[j] / data.lambda_0 for j in range(len(lambdas))]


def calculate_coefficients(alphas):
    return [data.nodes[j].channels_count * data.nodes[j].mu / alphas[j] for j in range(len(data.nodes))]


def calculate_rhos(lambdas):
    return [lambdas[j] / data.nodes[j].mu for j in range(len(lambdas))]


@dataclass
class PropertyQS:
    j: int | float
    n_o: int | float
    t_sys: int | float
    t_wait: int | float


def calculate_properties(probabilities_indices, probabilities):
    result = []
    for i in range(len(data.nodes)):
        j = sum([int(vector[i]) * probabilities[j] for j, vector in enumerate(probabilities_indices)])
        arr = [max(0, int(vector[i]) - data.nodes[i].channels_count) * probabilities[j] for j, vector in
               enumerate(probabilities_indices)]
        n_o = sum(arr)
        t_wait = n_o / (data.nodes[i].mu * (j - n_o))
        t_sys = j / (data.nodes[i].mu * (j - n_o))
        prop = PropertyQS(j=j, n_o=n_o, t_sys=t_sys, t_wait=t_wait)
        result.append(prop)
    return result


def build_equations():
    nodes_num = len(data.transmission_matrix)
    # variables = symbols("ω1 ω2 ω3 ω4")
    variables = symbols(" ".join([f"ω{i + 1}" for i in range(nodes_num)]))
    equations = [
        Eq(
            variables[j],
            sum([variables[i] * data.transmission_matrix[i][j] for i in range(nodes_num)])
        ) for j in range(nodes_num)
    ]
    return equations


def calculate_omegas(equations: list):
    nodes_num = len(data.transmission_matrix)
    variables = symbols(" ".join([f"ω{i + 1}" for i in range(nodes_num)]))
    solution = solve([*equations, Eq(sum(variables), 1)], dict=True)[0]
    result = [solution[variables[j]] for j in range(len(solution))]
    return result


def generate_probabilities_indices(n, length, current_sum=0, current_index=[], result=[]):
    if length == 0:
        if current_sum == n:
            result.append(tuple(current_index))
        return

    for num in range(n - current_sum + 1):
        generate_probabilities_indices(n, length - 1, current_sum + num, [*current_index, num], result)

    return result


def mu_i(i, k):
    return data.nodes[i].mu * min(k, data.nodes[i].channels_count)


def z_i(i, n_i, omegas):
    if n_i == 0:
        return 1
    result = 1
    result *= omegas[i] ** n_i
    result /= math.prod([mu_i(i, k) for k in range(1, n_i + 1)])
    return result


def calculate_probabilities(probabilities_indices: list[tuple], omegas: list):
    total = sum([state_z(n, omegas) for n in probabilities_indices])
    result = [float(state_z(n, omegas) / total) for n in probabilities_indices]
    return result


def state_z(n: tuple, omegas: list):
    requests_per_node = n
    result = math.prod([z_i(i=i, n_i=requests_per_node[i], omegas=omegas) for i in range(len(requests_per_node))])
    return result


class ClosedQSSystemSolver:
    def __init__(self):
        self.equations = build_equations()
        self.omegas = calculate_omegas(self.equations)
        self.probabilities_indices = generate_probabilities_indices(n=data.requests_number, length=len(
            data.transmission_matrix))

        self.probabilities = calculate_probabilities(self.probabilities_indices, self.omegas)

        reject_prob = sum([self.probabilities[i] for i, ind in enumerate(self.probabilities_indices) if ind[0] == 0])
        self.properties = calculate_properties(self.probabilities_indices, self.probabilities)
        self.total_property = PropertyQS(
            j=sum([p.j for p in self.properties]),
            n_o=sum([p.n_o for p in self.properties]),
            t_wait=sum([p.t_wait for p in self.properties]),
            t_sys=sum([p.t_sys for p in self.properties])
        )
