from abc import abstractmethod, ABC
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from shapely import Point
from sympy import Expr, Rational, Symbol

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds


@dataclass
class LinearPlotData(ABC):
    coeffs: list[Rational]
    const: float
    ax_bounds: AxBounds
    resolution: int
    color: str

    def __post_init__(self):
        if len(self.coeffs) != 2:
            raise ValueError("Incorrect LPP size")

    def y_value(self, x: float | np.ndarray):
        ax, ay = self.coeffs
        return (float(self.const) - float(ax) * x) / float(ay)

    def x_value(self, y: float):
        ax, ay = self.coeffs
        return (float(self.const) - float(ay) * y) / float(ax)

    @cached_property
    def x(self):
        start_x = max(self.ax_bounds.left_x, self.x_value(self.ax_bounds.bottom_y))
        end_x = min(self.ax_bounds.right_x, self.x_value(self.ax_bounds.top_y))
        return np.linspace(start_x, end_x, self.resolution)

    @cached_property
    def y(self):
        return self.y_value(self.x)

    def get_belonging_intersections(self, intersections: list[Point]) -> list[Point]:
        def is_point_belonging(_p: Point):
            tol = 1e-3
            point_coords = [_p.x, _p.y]
            result_value = sum([float(c_i) * p_i for c_i, p_i in zip(self.coeffs, point_coords)])
            expected_value = self.const
            diff = expected_value - result_value
            return abs(diff) < tol

        result = []

        for p in intersections:
            if is_point_belonging(p):
                result.append(p)
        return result

    def get_widest_section_indices(self, belonging_points: list[Point]) -> tuple[int, int]:
        points = belonging_points
        constraint_ends = [
            Point(float(self.x[0]), float(self.y[0])),
            Point(float(self.x[-1]), float(self.y[-1]))
        ]
        points.extend(constraint_ends)
        points = sorted(points, key=lambda pos: pos.x)

        def distance(pos1: Point, pos2: Point):
            x1, y1 = pos1.x, pos1.y
            x2, y2 = pos2.x, pos2.y
            dx = float(x2 - x1)
            dy = float(y2 - y1)
            return np.sqrt(dx ** 2 + dy ** 2)

        def widest_section_positions():
            max_distance = -1
            max_section_positions = []
            for i in range(1, len(points)):
                dist = distance(points[i - 1], points[i])
                if dist > max_distance:
                    max_distance = dist
                    max_section_positions = [points[i - 1], points[i]]
            return max_section_positions

        def find_nearest_pos_index(pos: Point) -> int:
            value = pos.x
            idx = (np.abs(self.x - value)).argmin()
            return idx

        section_sols = widest_section_positions()
        result = (find_nearest_pos_index(section_sols[0]), find_nearest_pos_index(section_sols[1]))
        return result

    @property
    @abstractmethod
    def annotation_text(self):
        pass
