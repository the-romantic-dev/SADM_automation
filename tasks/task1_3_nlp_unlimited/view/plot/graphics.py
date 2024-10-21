import numpy as np
import sympy as sp
from tasks.task1_3_nlp_unlimited.old.other.const import x1, x2

def level_lines(plt, expr, bounds):
    width = bounds["max"][0] - bounds["min"][0]
    hegith = bounds["max"][1] - bounds["min"][1]
    x1_vals = np.linspace(float(bounds["min"][0]) - float(width) * 0.05, float(bounds["max"][0]) + float(width) * 0.05, 1000)
    x2_vals = np.linspace(float(bounds["min"][1]) - float(hegith) * 0.05, float(bounds["max"][1]) + float(hegith) * 0.05, 1000)
    
    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    Z = sp.lambdify((x1, x2), expr, 'numpy')
    Z_values = Z(X1, X2)
    contours = plt.contour(X1, X2, Z_values, levels=200)  # levels - количество линий равного уровня

    # Добавляем подписи к осям и заголовок
    plt.xlabel('x1')
    plt.ylabel('x2')

    # Добавляем цветовую шкалу
    plt.colorbar(contours)
    

def dots_lines(plt, dots):
    for i in range(len(dots) - 1):
        plt.plot(
            [dots[i][0], dots[i+1][0]], 
            [dots[i][1], dots[i+1][1]],
            marker=' ',
            linestyle='-',
            color='red',
            label='Линии между точками')