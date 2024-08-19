from itertools import combinations

from shapely import Point

from tasks.task1_2_lp.view.plot.dataclasses.linear_funciton import LinearFunction


def determinant(A1, B1, A2, B2):
    """Вычисляет определитель для системы уравнений."""
    return A1 * B2 - A2 * B1


def find_intersection(lf1: LinearFunction, lf2: LinearFunction):
    """Находит точку пересечения двух линий методом Крамера, если она существует."""
    A1, B1, C1 = (lf1.x_coeff, lf1.y_coeff, lf1.const)
    A2, B2, C2 = (lf2.x_coeff, lf2.y_coeff, lf2.const)

    determinant_value = determinant(A1, B1, A2, B2)
    if determinant_value == 0:
        return None  # Линии параллельны, пересечения нет

    x = (C1 * B2 - C2 * B1) / determinant_value
    y = (A1 * C2 - A2 * C1) / determinant_value
    return x, y


def find_intersections(linear_functions: list[LinearFunction]) -> list[Point]:
    """Находит все точки пересечения для набора линейных функций."""
    result = []
    for lf1, lf2 in combinations(linear_functions, 2):
        intersection = find_intersection(lf1, lf2)
        if intersection is not None:
            x = intersection[0]
            y = intersection[1]
            result.append(Point(x, y))
    return list(set(result))


def filter_intersections_on_line(line: LinearFunction, intersections: list[Point]) -> list[Point]:
    """ Фильтрует заданные точки пересечения, чтобы найти те, которые лежат на указанной линейной функции. """
    coeffs = (line.x_coeff, line.y_coeff)

    def is_point_on_line(_p: Point):
        tol = 1e-3
        coords = [_p.x, _p.y]
        result_value = coeffs[0] * coords[0] + coeffs[1] * coords[1]
        expected_value = line.const
        diff = expected_value - result_value
        return abs(diff) < tol

    result = []

    for p in intersections:
        if is_point_on_line(p):
            result.append(p)
    return result
