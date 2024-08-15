from functools import cached_property

import numpy as np
from adjustText import adjust_text
from matplotlib.collections import PathCollection
from matplotlib.patches import Polygon
from matplotlib.transforms import Bbox
from scipy.spatial import ConvexHull
from sympy import pretty

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.view.plot.constraint_plot_data import ConstraintPlotData
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.dataclasses.position import Position
from tasks.task1_2_lp.view.plot.plot import Plot


class LPPPlot(Plot):
    def __init__(self, lpp: LPProblem, solutions: list[BasisSolution]):
        if lpp.var_count != 2:
            raise ValueError("Нельзя отобразить на графике ЗЛП где количество переменных не равно 2")
        self.ax_bounds = AxBounds.get_from_solutions(solutions, padding=5.0)
        self.lpp = lpp
        self.solutions = solutions
        self.objects = []
        super().__init__(self.ax_bounds)

    @cached_property
    def constraints_plot_data(self):
        result = []
        for constraint in self.lpp.constraints:
            cpd = ConstraintPlotData(constraint, resolution=1000, ax_bounds=self.ax_bounds)
            result.append(cpd)
        return result

    def add_all(self):
        self._add_constraints()
        self._add_constraints_annotations()
        self._add_acceptable_field_fill()
        self._add_solution_points()
        self._add_points_annotation()

    def _add_constraints(self):
        plot_data = self.constraints_plot_data
        for pd in plot_data:
            data = self.add_plot(x=pd.x, y=pd.y, color=pd.color)
            # self.objects.extend(data)

    def _add_constraints_annotations(self):
        plot_data = self.constraints_plot_data
        for pd in plot_data:
            belonging_solutions = pd.get_belonging_solutions(self.solutions)
            annotated_section = pd.get_widest_section_indices(belonging_solutions)
            mid_point = (annotated_section[0] + annotated_section[1]) // 2
            mid_x = float(pd.x[mid_point])
            mid_y = float(pd.y[mid_point])
            data = self.add_annotation(
                text=pd.constraint.pretty_str(),
                position=Position(x=mid_x, y=mid_y),
                angle=pd.angle(self.aspect),
                fill_color=pd.color,
                alpha=0.3
            )
            self.objects.append(data.get_window_extent())

    def _add_acceptable_field_fill(self):
        acceptable_sols = filter(lambda sol: sol.is_acceptable, self.solutions)
        positions = np.asarray([(float(sol.solution[0]), float(sol.solution[1])) for sol in acceptable_sols])
        hull = ConvexHull(positions)
        hull_points = positions[hull.vertices]
        data: list[Polygon] = self.add_fill(x=hull_points[:, 0], y=hull_points[:, 1], color='#FFB4BB', alpha=0.9)

        self.objects.extend([d.get_window_extent() for d in data])

    def _add_solution_points(self):
        positions = [Position(float(sol.solution[0]), float(sol.solution[1])) for sol in self.solutions]
        data = self.add_points(positions, size=50, color='#BAFFC9', z_order=3)
        box_half_width = 5

        def bbox(pos: Position):
            points = np.asarray([
                [pos.x - box_half_width, pos.y - box_half_width],
                [pos.x + box_half_width, pos.y + box_half_width]
            ])
            return Bbox(points=points)

        bboxes = [bbox(pos) for pos in positions]
        self.objects.extend(bboxes)

    def _add_points_annotation(self):
        annotations = []
        positions = [Position(float(sol.solution[0]), float(sol.solution[1])) for sol in self.solutions]
        for pos, sol in zip(positions, self.solutions):
            b1 = pretty(sol.basis_variables[0])
            b2 = pretty(sol.basis_variables[1])
            b1_value = sol.solution[sol.basis[0]]
            b2_value = sol.solution[sol.basis[1]]
            label = f"Базис: \n{b1} = {b1_value}\n{b2} = {b2_value}"
            annotation = self.add_annotation(label, pos, text_offset=(0, 0),
                                             arrow_properties=dict(facecolor='black', shrink=0.05))
            annotations.append(annotation)

        adjust_text(texts=annotations,
                    expand_text=(1, 1),
                    ha='center', va='top',
                    force_text=.6,
                    lim=277,
                    force_points=0.1,
                    objects=self.objects)
