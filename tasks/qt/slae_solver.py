import sympy as sp
from matplotlib import pyplot as plt


class QTSLAESolver:
    def task_A17А_solve(self, lamb, t):
        lamb_value = lamb / 60
        mu_value = 1 / t
        P = [sp.symbols(f"P{i}") for i in range(15 + 1)]
        equations = [
            *[P[i] - (lamb_value / mu_value) * P[i - 1] for i in range(1, 4 + 1)],
            P[5] - (lamb_value / (2 * mu_value)) * P[4],
            *[P[i] - (lamb_value / (3 * mu_value)) * P[i - 1] for i in range(6, 15 + 1)],
            sum(P) - 1
        ]
        solution = sp.solve(equations, P)
        Ps = lambda i: solution[P[i]]
        average_queue = Ps(2) + 2 * Ps(3) + 3 * (
                sum([Ps(i) for i in range(3, 6 + 1)]) + sum([(i - 3) * Ps(i) for i in range(7, 15 + 1)]))
        return solution, average_queue

    def task_20_solve(self, lamb, mu, K):
        P1 = [sp.symbols(f"P{i}") for i in range(K + 1)]
        equations1 = [
            *[P1[i + 1] - (lamb / mu) * P1[i] for i in range(K)],
            sum(P1) - 1

        ]
        solution1 = sp.solve(equations1, P1)
        P2 = [sp.symbols(f"P{i}") for i in range(K + 2)]
        equations2 = [
            *[P2[i + 1] - (lamb / mu) * P2[i] for i in range(K + 1)],
            sum(P2) - 1

        ]
        solution2 = sp.solve(equations2, P2)
        P_rab_1 = sum(i * solution1[P1[i]] for i in range(len(P1)))
        P_rab_2 = sum(i * solution2[P2[i]] for i in range(len(P2)))
        return solution1, solution2, (P_rab_1, P_rab_2)


solver = QTSLAESolver()
# solution, ae = solver.task_A17А_solve(
#     lamb=10, t=12
# )
# for v in solution:
#     print(f"{v}: {round(solution[v], 4)}")
# print(ae)
task2_solution = solver.task_20_solve(
    lamb=0.8, mu=2, K=5
)
p1 = []
p2 = []
for v in task2_solution[0]:
    p1.append(f"{v}: {round(task2_solution[0][v], 4)}")

for v in task2_solution[1]:
    p1.append(f"{v}: {round(task2_solution[1][v], 4)}")

for p in p1:
    print(p)

for p in p2:
    print(p)

print(task2_solution[2])
A1 = lambda z: 264.2 + 0.0357 * z
A2 = lambda z: 265.52 + 0.0144 * z
x_values = list(range(0, 10**5))  # от -10 до 10
A1_values = [A1(z) for z in x_values]
A2_values = [A2(z) for z in x_values]

# Строим графики
plt.plot(x_values, A1_values, label='A1')
plt.plot(x_values, A2_values, label='A2')

plt.xlabel('z')
plt.ylabel('Общая цена')
plt.legend()

# Показываем график
plt.grid(True)
# plt.axhline(0, color='black', linewidth=0.5)
# plt.axvline(0, color='black', linewidth=0.5)
plt.show()