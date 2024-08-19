import numpy as np
from shapely import Point


def distance(p1: Point, p2: Point):
    """ Расстояние между двумя точками """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    dx = float(x2 - x1)
    dy = float(y2 - y1)
    return np.sqrt(dx ** 2 + dy ** 2)


def find_widest_line_segment(on_line_points: list[Point]) -> tuple[Point, Point]:
    sorted_points = sorted(on_line_points, key=lambda p: p.x)
    max_distance = -1
    widest_segment = []
    for i in range(1, len(sorted_points)):
        dist = distance(sorted_points[i - 1], sorted_points[i])
        if dist > max_distance:
            max_distance = dist
            widest_segment = [sorted_points[i - 1], sorted_points[i]]
    return tuple(widest_segment)
