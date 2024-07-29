import math
import sympy as sp


def solve_2(T: int, K: int, m: int, N: int):
    lamb = 10
    mu = K
    nu = 1 / T
    rho = lamb / mu
    # Нормированная интенсивность уходов
    beta = nu / mu


def solve_AC9(N, K, M, R):
    lamb = K
    mu = M
    rho = lamb / mu
    rho_2 = 0.8 * rho

    def before_R_factor(j):
        return (math.factorial(N) * rho ** j) / (math.factorial(N - j) * math.factorial(j))

    def from_R_to_2r_factor(j):
        return (math.factorial(N) * rho ** j) / (math.factorial(N - j) * math.factorial(R) * R ** (j - R))

    def after_2R_factor(j):
        return (math.factorial(N) * rho_2 ** j) / (math.factorial(N - j) * math.factorial(R) * R ** (j - R))

    def P0():
        first = []
        for j in range(1, R + 1):
            first.append(before_R_factor(j))
        second = []
        for j in range(R + 1, 2 * R + 1):
            second.append(from_R_to_2r_factor(j))
        third = []
        for j in range(2 * R + 1, N + 1):
            third.append(after_2R_factor(j))
        return round(sum(first), 6), round(sum(second), 6), round(sum(third), 6)

    P0_result = P0()
    print(f"Слагаемые знаменателя P0: {P0_result}")
    print(f"Сумма слагаемых: {sum(P0_result)}")

    P0_value = round(1 / (1 + sum(P0_result)), 4)
    print(f"P0: {P0_value}")

    def Pj(j):
        if j <= R:
            return before_R_factor(j) * P0_value
        elif K < j <= 2 * R:
            return from_R_to_2r_factor(j) * P0_value
        elif j > 2 * R:
            return after_2R_factor(j) * P0_value
        else:
            raise ValueError("Хуета")

    def n0():
        result = 0
        for j in range(R + 1, N + 1):
            result += (j - R) * Pj(j)
        return result

    def K3():
        result_1 = 0
        for j in range(1, R):
            result_1 += j * Pj(j)
        result_2 = 0
        for j in range(R, N + 1):
            result_2 += R * Pj(j)
        return result_1, result_2

    Pj_results = [Pj(j) for j in range(1, N + 1)]
    for j in range(len(Pj_results)):
        print(f"P{j + 1} = {Pj_results[j]}")
    print(f"n0 = {n0()}")
    K3_result = K3()
    print(f"K3 = {K3_result[0]} + {K3_result[1]} = {sum(K3_result)}")
    j = sum(K3_result) + n0()
    print(f"j = {j}")
    t_c = j / (lamb * (N - j))
    t_ozh = n0() / (lamb * (N - j))
    print(f"t_c = {t_c}")
    print(f"t_ож = {t_ozh}")

solve_AC9(10, 0.05, 0.5, 3)
