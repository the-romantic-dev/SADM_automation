import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, Eq, solve

mu = symbols("μ")
nu = symbols("ν")
P = symbols("P0 P1 P2 P3 P4 P5 P6 P7 P8 P9 P10")

equations = [
    Eq(2 * mu / nu * (P[1] + P[2] + P[3] + P[4]), P[0]),
    Eq((mu * (P[5] + P[8]) + nu / 2 * P[0]) / (mu + nu), P[1]),
    Eq((mu * (P[6] + P[10]) + nu / 2 * P[0]) / (mu + nu), P[2]),
    Eq((mu * (P[6] + P[7]) + nu / 2 * P[0]) / (mu + nu), P[3]),
    Eq((mu * (P[5] + P[9]) + nu / 2 * P[0]) / (mu + nu), P[4]),
    Eq(nu / (4 * mu) * (P[1] + P[4]), P[5]),
    Eq(nu / (4 * mu) * (P[2] + P[3]), P[6]),
    Eq(nu / (2 * mu) * P[1], P[7]),
    Eq(nu / (2 * mu) * P[3], P[8]),
    Eq(nu / (2 * mu) * P[2], P[9]),
    Eq(nu / (2 * mu) * P[4], P[10]),
    Eq(sum(P), 1)
]

result = solve(equations, P[0], dict=True)
print(result)

