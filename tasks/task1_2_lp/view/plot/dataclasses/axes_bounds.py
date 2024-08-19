from dataclasses import dataclass

from shapely import Point

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution


@dataclass
class AxesBounds:
    left_x: int | float
    right_x: int | float
    top_y: int | float
    bottom_y: int | float

    @staticmethod
    def get_from_solutions(solutions: list[BasisSolution], padding: float):
        max_x1 = max([sol.solution[0] for sol in solutions])
        max_x2 = max([sol.solution[1] for sol in solutions])
        min_x1 = min([sol.solution[0] for sol in solutions])
        min_x2 = min([sol.solution[1] for sol in solutions])
        return AxesBounds(
            left_x=float(min_x1) - padding,
            right_x=float(max_x1) + padding,
            bottom_y=float(min_x2) - padding,
            top_y=float(max_x2) + padding
        )

    def contains(self, point: Point):
        return self.left_x <= point.x <= self.right_x and self.top_y >= point.y >= self.bottom_y
