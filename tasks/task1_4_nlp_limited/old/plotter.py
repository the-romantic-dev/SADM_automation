import matplotlib.pyplot as plt
from numpy import linspace, meshgrid, full, clip
from sympy import lambdify, symbols, solve, Matrix, linsolve, simplify, diff
from scipy.spatial import ConvexHull
from util import is_X_allowed

x1, x2 = symbols("x1 x2")
margin_coefficient = 0.05

def calculate_max_min_dots(dots) -> dict:
    """Поиск границ plot по крайним точкам графика"""
    min_x1 = None
    min_x2 = None
    max_x1 = None
    max_x2 = None

    for d in dots:
        d = d.T.tolist()[0]
        if min_x1 is None or min_x1 > d[0]:
            min_x1 = d[0]
        if min_x2 is None or min_x2 > d[1]:
            min_x2 = d[1]
        if max_x1 is None or max_x1 < d[0]:
            max_x1 = d[0]
        if max_x2 is None or max_x2 < d[1]:
            max_x2 = d[1]

    return {"min": [min_x1, min_x2], "max": [max_x1, max_x2]}


def get_quadratis_limits_extreme_points(quadratic_limits):
    result = []
    for i in range(len(quadratic_limits)):
        vertical = solve(quadratic_limits[i].subs({x1: 0}), x2)
        horizontal = solve(quadratic_limits[i].subs({x2: 0}), x1)
        result.append(Matrix([0, vertical[0]]))
        result.append(Matrix([0, vertical[1]]))
        result.append(Matrix([horizontal[0], 0]))
        result.append(Matrix([horizontal[1], 0]))
    return result


def get_linear_limits_intersects(linear_limits) -> list:
    points = []
    for i in range(len(linear_limits)):
        for j in range(len(linear_limits)):
            if i != j:
                try:
                    intersection = list(linsolve([linear_limits[i], linear_limits[j]], (x1, x2)))[0]
                    matrix = Matrix([intersection[0], intersection[1]])
                    if is_X_allowed(matrix, linear_limits):
                        if matrix not in points:
                            points.append(matrix)
                except IndexError:
                    continue
    # Преобразуем список точек в порядке для построения выпуклой оболочки
    points = [(point[0, 0], point[1, 0]) for point in points]
    hull = ConvexHull(points=points)
    result = [Matrix(points[i]) for i in hull.vertices]
    return result


def get_limits_degree(limits):
    if simplify(limits[0]).is_polynomial():
        degree = simplify(limits[0]).as_poly().degree()
    else:
        raise ValueError("Ограничения не являются линейными или квадратичными")
    return degree


def get_limits_points(limits):
    degree = get_limits_degree(limits)
    match degree:
        case 1:
            return get_linear_limits_intersects(limits)
        case 2:
            return get_quadratis_limits_extreme_points(limits)


def add_limits(limits, bounds):
    degree = get_limits_degree(limits)
    match degree:
        case 1:
            return add_linear_limitations(limits)
        case 2:
            return add_quadratic_limitations(limits, bounds)


def _get_plot_vars_values(bounds):
    width = bounds["max"][0] - bounds["min"][0]
    hegith = bounds["max"][1] - bounds["min"][1]
    x1_vals = linspace(
        float(bounds["min"][0]) - float(width) * margin_coefficient,
        float(bounds["max"][0]) + float(width) * margin_coefficient,
        1000,
    )
    x2_vals = linspace(
        float(bounds["min"][1]) - float(hegith) * margin_coefficient,
        float(bounds["max"][1]) + float(hegith) * margin_coefficient,
        1000,
    )
    return x1_vals, x2_vals


def add_level_lines(expr, bounds):
    x1_vals, x2_vals = _get_plot_vars_values(bounds)
    X1, X2 = meshgrid(x1_vals, x2_vals)
    Z = lambdify((x1, x2), expr, "numpy")
    Z_values = Z(X1, X2)
    contours = plt.contour(
        X1, X2, Z_values, levels=100
    )  # levels - количество линий равного уровня

    # Добавляем цветовую шкалу
    plt.colorbar(contours)


def add_quadratic_limitations(limitations, bounds):
    x1_vals, x2_vals = _get_plot_vars_values(bounds)
    X1, X2 = meshgrid(x1_vals, x2_vals)

    for lim in limitations:
        Z = lambdify((x1, x2), lim, "numpy")
        Z_values = Z(X1, X2)
        plt.contour(
            X1, X2, Z_values, levels=[0], color='black'
        )


def add_linear_limitations(limitations):
    intersects = get_linear_limits_intersects(limitations)
    for i in range(len(intersects) - 1):
        plt.plot(
            [intersects[i][0, 0], intersects[i + 1][0, 0]],
            [intersects[i][1, 0], intersects[i + 1][1, 0]],
            marker=' ',
            linestyle='-',
            color='black')
    plt.plot(
        [intersects[0][0, 0], intersects[-1][0, 0]],
        [intersects[0][1, 0], intersects[-1][1, 0]],
        marker=' ',
        linestyle='-',
        color='black')


def add_linear_eq_limitation(limitation, bounds):
    a = diff(limitation, x1)
    b = diff(limitation, x2)
    c = a * x1 + b * x2 - limitation

    width = bounds["max"][0] - bounds["min"][0]
    hegith = bounds["max"][1] - bounds["min"][1]

    start_x1 = float(bounds["min"][0]) - float(width) * margin_coefficient,
    end_x1 = float(bounds["max"][0]) + float(width) * margin_coefficient

    start_x2 = float(bounds["min"][1]) - float(hegith) * margin_coefficient,
    end_x2 = float(bounds["max"][1]) + float(hegith) * margin_coefficient,
    if b != 0:
        # Создайте массив значений x1 в заданном диапазоне
        x1_values = linspace(start_x1, end_x1, 100)

        # Выразите x2 через x1, используя уравнение a*x1 + b*x2 = c
        x2_values = (c - a * x1_values) / b
        x2_values = clip(x2_values, start_x2, end_x2)
        # Постройте график
        if a != 0:
            plt.plot(x1_values, x2_values, label=f'{a}*x1 + {b}*x2 = {c}')
        else:
            plt.plot(x1_values, x2_values, label=f'{b}*x2 = {c}')
    else:
        # Для случая b = 0, построим вертикальную линию
        x1_values = full(100, c / a)
        x2_values = linspace(start_x2, end_x2, 100)
        plt.plot(x1_values, x2_values, label=f'{a}*x1 = {c}')

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()


def add_solution_track(track):
    for i in range(len(track) - 1):
        plt.plot(
            [track[i][0, 0], track[i + 1][0, 0]],
            [track[i][1, 0], track[i + 1][1, 0]],
            marker='.',
            linestyle='-',
            color='red')


def show():
    # Добавляем подписи к осям
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.show()


def save(path: str):
    plt.savefig(path)


def clear():
    bounds = None
    plt.clf()
