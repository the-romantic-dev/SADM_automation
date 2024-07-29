import math

import matplotlib.pyplot as plt

lamb = 0.8
mu = 0.2
rho = lamb / mu
S = 10000
s1 = 200
s2 = 100
z = 20
q = 0.01


def P0(N):
    result = 1
    for j in range(1, N + 1):
        result += rho ** j / math.factorial(j)
    return result ** -1


def Pj(j, N):
    return P0(N) * rho ** j / math.factorial(j)

def P_rej(N):
    return Pj(N, N)


def k3(N):
    return rho * (1 - P_rej(N))


def A(N):
    result = 0
    result += S * N / 100
    result += s1 * k3(N)
    result += s2 * (N - k3(N))
    result += z * q * lamb * 60 * 24 * P_rej(N)
    return result


min_N = 0
N_num = 10
N_range = [i + min_N for i in range(N_num)]
f_range = [A(i) for i in N_range]

for i in range(len(N_range)):
    if f_range[i] < 0.01:
        print(f"A(N) = {f_range[i - 1]} при N = {N_range[i - 1]}")
        print(f"A(N) = {f_range[i]} при N = {N_range[i]}")
        break

plt.plot(N_range, f_range, label="A(N)")
plt.xlabel("Количество аппаратов")
plt.xticks(N_range)
plt.ylabel("Цена содержания системы контроля")
plt.yticks(f_range)
plt.grid()
plt.legend()
plt.show()
