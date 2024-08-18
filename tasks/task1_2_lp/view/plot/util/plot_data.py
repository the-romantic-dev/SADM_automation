from dataclasses import dataclass
from functools import cached_property

import numpy as np
from shapely import Point
from sympy import Expr, Rational, Symbol

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds


@dataclass
class LinearPlotData:
    coeffs: list[Rational]
    const: float
    ax_bounds: AxBounds
    resolution: int
    expr: Expr
    variables: list[Symbol]
    color: str

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

    def angle(self, aspect: float) -> float:
        """ Угол графика в градусах. Зависит от размерности aspect всего plot-a"""
        dx = self.x[-1] - self.x[0]
        dy = self.y[-1] - self.y[0]
        return np.degrees(np.arctan2(dy * aspect, dx))

    def get_belonging_solutions(self, solutions: list[BasisSolution]) -> list[BasisSolution]:
        def is_sol_belonging(_sol: BasisSolution):
            tol = 1e-3
            solution = _sol.solution
            variables = self.variables
            expr: Expr = self.expr
            result_value = float(expr.subs({variables[i]: solution[i] for i in range(len(variables))}))
            expected_value = self.const
            diff = expected_value - result_value
            return abs(diff) < tol

        result = []

        for sol in solutions:
            if is_sol_belonging(sol):
                result.append(sol)
        return result

    def get_widest_section_indices(self, belonging_solutions: list[BasisSolution]) -> tuple[int, int]:
        points = [Point(sol.solution[0], sol.solution[1]) for sol in belonging_solutions]
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
