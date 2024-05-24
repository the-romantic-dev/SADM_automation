import numpy as np
from matplotlib import pyplot as plt
from sympy import Eq, symbols, solve, simplify, lambdify

# P = {
#     "000": symbols("P_000"),
#     "001": symbols("P_001"),
#     "010": symbols("P_010"),
#     "011": symbols("P_011"),
# }
rho, alpha, phi = symbols("ρ α φ")
# equations = [
#     Eq(P["001"], rho * (1 + alpha) * (1 - phi) / alpha * P["000"]),
#     Eq(P["010"], rho * phi * (1 + alpha) * P["000"]),
#     Eq(P["011"], rho ** 2 * (1 + alpha) ** 2 / alpha * P["000"]),
#     Eq(P["000"] + P["001"] + P["010"] + + P["011"] / (1 - rho), 1)
# ]

# solution = solve(equations, [P["000"], P["001"], P["010"], P["011"]], dict=True)[0]
# j = simplify(solution[P["001"]] + solution[P["010"]] + 2 * solution[P["011"]] / (1 - rho))


j = (rho * (1 + alpha))/((1 - rho) ** 2 * (phi * (1 - alpha) + alpha))
j = simplify(j.subs({rho: 0.6}))
alpha_values = np.linspace(0, 1, 100)
phi_values = np.linspace(0, 1, 100)

X, Y = np.meshgrid(alpha_values, phi_values)
Z = lambdify((alpha, phi), j, "numpy")
Z_values = Z(X, Y)
# contours = plt.contour(
#         X, Y, Z_values, levels=100
# )
# plt.xlabel("α")
# plt.ylabel("φ")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z_values)
ax.set_xlabel('α')
ax.set_ylabel('φ')
ax.set_zlabel('j = f(α, φ)')
plt.show()


plt.colorbar()
plt.show()
