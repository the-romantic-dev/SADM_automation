import math
from shapely import Point

from tasks.task1_2_lp.view.plot.util.annotation_rectangle import AnnotationRectangle


class Contur:
    def __init__(self, rectangle: AnnotationRectangle, radius: float):
        self.anchor = rectangle.anchor_point
        self.rectangle = rectangle
        self.radius = radius

    def center_distance(self, angle: float):
        if angle > 2 * math.pi or angle < 0:
            raise ValueError("Incorrect angle")
        result = self.radius
        w = self.rectangle.width
        h = self.rectangle.height
        beta = math.atan(h / w)
        is_line_cross_vertical = (
                0 <= angle <= beta or
                math.pi - beta <= angle <= math.pi or
                2 * math.pi - beta <= angle <= 2 * math.pi or
                math.pi <= angle <= math.pi + beta
        )
        if is_line_cross_vertical:
            l = w / (2 * abs(math.cos(angle)))
        else:
            l = h / (2 * abs(math.sin(angle)))

        return result + l

    def points(self, resolution: int) -> list[Point]:
        points = []

        for i in range(resolution):
            angle = 2 * math.pi * (i / resolution)
            R = self.center_distance(angle)
            x_offset = R * math.cos(angle)
            y_offset = R * math.sin(angle)
            x = self.anchor.x + x_offset
            y = self.anchor.y + y_offset
            points.append(Point(x, y))
        return points
