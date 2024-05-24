import sympy as sp
from matplotlib import pyplot as plt

rho = sp.symbols("ρ")
phi = sp.symbols("φ")
alpha = sp.symbols("α")
P000 = sp.symbols("P000")
P010 = sp.symbols("P010")
P001 = sp.symbols("P001")
P011 = sp.symbols("P011")
equations = [
    sp.Eq(P010, P000 * rho * phi * (1 + alpha)),
    sp.Eq(P001, P000 * rho * (1 + alpha) * (1 - phi) / alpha),
    sp.Eq(P011, P000 * rho ** 2 * (1 + alpha)**2 / alpha),
    sp.Eq(P000 + P001 + P010 + P011 / (1 - rho), 1)
]
solution = sp.solve(equations, [P000, P010, P001, P011], dict=True)[0]
for s in solution:
    print(f"{sp.pretty(s)}:")
    print(solution[s])
print(solution[P000].subs({alpha: 1}))

