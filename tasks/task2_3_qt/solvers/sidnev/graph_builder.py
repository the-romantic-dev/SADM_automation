import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, solve, Eq, simplify

lamb = 10
mu = 10
nu = symbols("ν")
p0, p1, p2, p3 = symbols("p0 p1 p2 p3")

equations = [
    Eq(p1, p0 * lamb / (mu + nu)),
    Eq(p2, p1 * lamb / (2 * mu + 2 * nu)),
    Eq(p3, p2 * lamb / (2 * mu + 3 * nu)),
    Eq(p0 + p1 + p2 + p3, 1)
]
solution = solve(equations, p0, p1, p2, p3, dict=True)[0]
j = simplify(solution[p1] + 2 * solution[p2] + 3 * solution[p3])
P_rej = solution[p3]
P_esc = j * nu / lamb
P = simplify(P_rej + P_esc)
t3 = symbols("t3")
# func = (1.2 * nu + 32 * nu ** 2 + 148 * nu + 200) / (11 * nu ** 2 + 190 * nu + 800)
func = P.subs({nu: 1 / t3})
nu_values = np.linspace(0.1, 1, 100)
func_values = [func.subs({t3: val}) for val in nu_values]
print(func_values[0])
print(func_values[-1])
plt.plot(nu_values, func_values, label="Pпот")
plt.xlabel("t3")
plt.ylabel("P")
plt.legend()
plt.show()
