import math
from dataclasses import dataclass

import tasks.task2_4_qt_sys.open_systems.data as data
from sympy import symbols, Eq, Rational
from sympy.solvers import solve


def calculate_lambdas(equations: list):
    solution = solve(equations, dict=True)[0]
    result = [solution[symbols(f"λ{j + 1}")] for j in range(len(solution))]
    return result


def calculate_alphas(lambdas):
    return [lambdas[j] / data.lambda_0 for j in range(len(lambdas))]


def calculate_coefficients(alphas):
    return [data.nodes[j].channels_count * data.nodes[j].mu / alphas[j] for j in range(len(data.nodes))]


def calculate_rhos(lambdas):
    return [lambdas[j] / data.nodes[j].mu for j in range(len(lambdas))]


def calc_P0(rho, k):
    result = 1
    for j in range(1, k + 1):
        result += rho ** j / math.factorial(j)
    result += rho ** (k + 1) / (math.factorial(k) * (k - rho))
    return result ** -1


def calc_n_o(rho, k, P0):
    rho_c = rho / k
    return rho ** (k + 1) * P0 / (math.factorial(k) * k * (1 - rho_c) ** 2)


@dataclass
class PropertyQS:
    j: int | float
    n_o: int | float
    t_sys: int | float
    t_wait: int | float


def calculate_properties(rhos):
    result = []
    for i in range(len(data.nodes)):
        rho = rhos[i]
        lamb = rho * data.nodes[i].mu
        k = data.nodes[i].channels_count
        P0 = calc_P0(rho, k)
        n_o = calc_n_o(rho, k, P0)
        j = n_o + rho
        t_wait = n_o / lamb
        t_sys = j / lamb
        prop = PropertyQS(j=j, n_o=n_o, t_sys=t_sys, t_wait=t_wait)
        result.append(prop)
    return result


def build_equations():
    def lamb(k):
        if k == 0:
            return data.lambda_0
        else:
            return variables[k - 1]

    variables = symbols("λ1 λ2 λ3 λ4")
    equations = [
        Eq(
            lamb(j),
            sum([lamb(i) * data.transmission_matrix[i][j] for i in range(0, 5)])
        ) for j in range(0, 5)
    ]
    return equations


class OpenQSSystemSolver:
    def __init__(self):
        self.equations = build_equations()
        self.lambdas = calculate_lambdas(self.equations)
        self.alphas = calculate_alphas(self.lambdas)
        self.coefficients = calculate_coefficients(self.alphas)
        self.rhos = calculate_rhos(self.lambdas)
        self.properties = calculate_properties(self.rhos)
        self.total_property = PropertyQS(
            j=sum([p.j for p in self.properties]),
            n_o=sum([p.n_o for p in self.properties]),
            t_wait=sum([p.t_wait * self.alphas[i] for i, p in enumerate(self.properties)]),
            t_sys=sum([p.t_sys * self.alphas[i] for i, p in enumerate(self.properties)])
        )
