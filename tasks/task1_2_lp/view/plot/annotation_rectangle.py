from typing import Self

import numpy as np
from matplotlib.axes import Axes
from matplotlib.text import Annotation
from shapely import box, Polygon, Point, LineString
from shapely.affinity import translate
from shapely.ops import split


def rectangle(annotation: Annotation, ax: Axes, margin: float) -> Polygon:
    pixel_bbox = annotation.get_window_extent()
    x0, y0, width, height = pixel_bbox.bounds
    inv_transform = ax.transData.inverted()
    points = np.array([[x0, y0], [x0 + width, y0 + height]])
    inv_points = list(inv_transform.transform(points))
    result = box(
        xmin=inv_points[0][0] - margin / 2,
        ymin=inv_points[0][1] - margin / 2,
        xmax=inv_points[1][0] + margin / 2,
        ymax=inv_points[1][1] + margin / 2)
    return result


class AnnotationRectangle:
    def __init__(self, annotation: Annotation, ax: Axes, margin: float):
        self.ax = ax
        self.annotation = annotation
        self.polygon = rectangle(annotation, ax, margin)

    @property
    def anchor_point(self) -> Point:
        return Point(self.annotation.xy[0], self.annotation.xy[1])

    @property
    def area(self) -> float:
        return self.polygon.area

    @property
    def center(self) -> Point:
        return self.polygon.centroid

    @center.setter
    def center(self, new_center: Point):
        current_center = self.center
        offset_x = new_center.x - current_center.x
        offset_y = new_center.y - current_center.y
        moved_rectangle: Polygon = translate(geom=self.polygon, xoff=offset_x, yoff=offset_y)
        self.polygon = moved_rectangle

    @property
    def width(self):
        minx, _, maxx, _ = self.polygon.bounds

        width = maxx - minx
        return width

    @property
    def height(self):
        _, miny, _, maxy = self.polygon.bounds

        height = maxy - miny
        return height

    def intersection_area(self, obj: Self | LineString):
        if isinstance(obj, LineString):
            return self.line_intersection_area(obj)
        elif isinstance(obj, AnnotationRectangle):
            return self.rectangle_intersection_area(obj)
        else:
            raise TypeError("Incorrect obj type")

    def line_intersection_area(self, line: LineString) -> float:
        geoms = split(self.polygon, line).geoms
        if len(geoms) < 2:
            return 0
        polygon1, polygon2 = geoms
        area1 = polygon1.area
        area2 = polygon2.area
        return min(area1, area2)

    def rectangle_intersection_area(self, other: Self) -> float:
        intersection = self.polygon.intersection(other.polygon)
        if intersection.is_empty:
            return 0
        return intersection.area
