import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, e
def df_nonl(x, y):
    # return [1 - pow(x, 2) - pow(y, 2), 2 * x]
    return [sqrt((x - y)**2 + 3) - 2, e**(y**2 - x) - e]

X, Y = np.meshgrid(np.linspace(-2, 5, 25), np.linspace(-5, 5, 25))
u, v = np.zeros(X.shape), np.zeros(Y.shape)
n, m = X.shape

for i in range(n):
    for j in range(m):
        x, y = X[i, j], Y[i, j]
        f_nonl = df_nonl(x, y)
        u[i, j] = f_nonl[0]
        v[i, j] = f_nonl[1]

plt.streamplot(X, Y, u, v, color='black', density=2, linewidth=1, arrowsize=0.7)
plt.ylabel("y(t)")
plt.xlabel("x(t)")
plt.axis("square")
plt.axis([-2, 5, -2, 5])
plt.show()
