from shapely import LineString

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds


class ObjectiveLine:
    def __init__(self, objective: Objective, opt_sol: BasisSolution):
        self.objective = objective
        self.ax = float(objective.coeffs[0])
        self.ay = float(objective.coeffs[1])
        self.const = float(opt_sol.objective_value)

    def x(self, y: float) -> float | None:
        if self.ax == 0:
            return None
        return (self.const - self.ay * y) / self.ax

    def y(self, x: float) -> float | None:
        if self.ay == 0:
            return None
        return (self.const - self.ax * x) / self.ay

    def line_string(self, ax_bounds: AxBounds) -> LineString:

        left_y = self.y(ax_bounds.left_x)
        right_y = self.y(ax_bounds.right_x)
        if left_y is None or right_y is None:
            y0 = ax_bounds.bottom_y
            y1 = ax_bounds.top_y
            x0 = self.x(y0)
            x1 = self.x(y1)
        else:
            y0 = left_y
            y1 = right_y
            x0 = ax_bounds.left_x
            x1 = ax_bounds.right_x

        return LineString([[x0, y0], [x1, y1]])