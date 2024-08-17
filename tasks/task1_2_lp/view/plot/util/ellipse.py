import math
from shapely import Point


class Ellipse:
    def __init__(self, center: Point, width: float, height: float):
        self.center = center
        self.height = height
        self.width = width

    def points(self, resolution: int) -> list[Point]:
        half_width = self.width / 2
        half_height = self.height / 2
        points = []

        for i in range(resolution):
            angle = 2 * math.pi * (i / resolution)
            x = self.center.x + half_width * math.cos(angle)
            y = self.center.y + half_height * math.sin(angle)
            points.append(Point(x, y))
        return points
