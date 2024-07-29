import math

import matplotlib.pyplot as plt
import numpy as np

lamb = 5
mu = 1 / 2
rho = lamb / mu


def P0(N):
    result = 1
    for j in range(1, N + 1):
        result += rho ** j / math.factorial(j)
    result += rho ** (N + 1) / (math.factorial(N) * (N - rho))
    return result ** -1


def f(N):
    result = 0
    for j in range(N):
        result += rho ** j / math.factorial(j)
    return P0(N) * result


def f_2(N):
    return 0.9 * math.e ** (-mu * (N - rho))


min_N = 11
N_num = 10
N_range = [i + min_N for i in range(N_num)]
f_range = [f_2(i) for i in N_range]

for i in range(len(N_range)):
    if f_range[i] < 0.01:
        print(f"f(N) = {f_range[i - 1]} при N = {N_range[i - 1]}")
        print(f"f(N) = {f_range[i]} при N = {N_range[i]}")
        break


plt.plot(N_range, f_range, label="f(N)")
plt.plot(N_range, [0.01 for i in N_range], label="f(N) = 0.01")
plt.xlabel("N")
plt.xticks(N_range)
plt.ylabel("f(N)")
plt.legend()
plt.show()
