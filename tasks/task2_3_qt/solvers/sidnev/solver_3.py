import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, lambdify


def build_graphs(x, y, z: tuple, levels: int):
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    cp1 = plt.contour(x, y, z[0], levels=levels, cmap='plasma')
    plt.clabel(cp1, inline=True, fontsize=8)
    plt.title("P_пот_I")
    plt.xlabel("ρ1")
    plt.ylabel("ρ2")

    plt.subplot(1, 2, 2)
    cp2 = plt.contour(x, y, z[1], levels=levels, cmap='plasma')
    plt.clabel(cp2, inline=True, fontsize=8)
    plt.title("P_пот_II")
    plt.xlabel("ρ1")
    plt.ylabel("ρ2")

    plt.tight_layout()


rho1, rho2 = symbols("ρ1 ρ2")
P_pot_I = (rho1 ** 2 / 2 + rho2) / (1 + rho1 + rho2 + rho1 ** 2 / 2)
P_pot_II = (rho1 ** 2 / 2 + rho2 + rho1) / (1 + rho1 + rho2 + rho1 ** 2 / 2)

rho1_values = np.linspace(0, 1, 100)
rho2_values = np.linspace(0, 1, 100)

X, Y = np.meshgrid(rho1_values, rho2_values)
Z1 = lambdify((rho1, rho2), P_pot_I, "numpy")
Z2 = lambdify((rho1, rho2), P_pot_II, "numpy")
Z1_values = Z1(X, Y)
Z2_values = Z2(X, Y)

build_graphs(x=X, y=Y, z=(Z1_values, Z2_values), levels=25)

plt.show()

rho = symbols("ρ")
P_pot = rho ** 2 / 2 / (1 + rho + rho ** 2 / 2)
rho_values = np.linspace(0, 2, 100)
P_pot_values = [P_pot.subs({rho: i}) for i in rho_values]
plt.plot(rho_values, P_pot_values)
plt.title("P_пот")
plt.xlabel("ρ")
plt.ylabel("P")

plt.show()
