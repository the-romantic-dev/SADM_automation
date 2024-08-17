from functools import cached_property

import numpy as np
from matplotlib.text import Annotation
from scipy.spatial import ConvexHull
from shapely import Point
from sympy import pretty

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem

from tasks.task1_2_lp.view.plot.util.annotation_rectangle import AnnotationRectangle
from tasks.task1_2_lp.view.plot.util.constraint_line import ConstraintLine
from tasks.task1_2_lp.view.plot.util.constraint_plot_data import ConstraintPlotData
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.ellipse import Ellipse
from tasks.task1_2_lp.view.plot.plot import Plot


class LPPPlot(Plot):
    def __init__(self, lpp: LPProblem, solutions: list[BasisSolution]):
        if lpp.var_count != 2:
            raise ValueError("Нельзя отобразить на графике ЗЛП где количество переменных не равно 2")
        self.ax_bounds = AxBounds.get_from_solutions(solutions, padding=5.0)
        self.lpp = lpp
        self.solutions = solutions
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

    def _adjust_annotations(self, annotations: list[Annotation], offset_radius: float):
        constraints = self.lpp.constraints + Constraint.get_non_negative_constraints(vars_count=2)
        lines = [ConstraintLine(constraint).line_string(self.ax_bounds) for constraint in constraints]
        rectangles = [AnnotationRectangle(annotations[i], self.ax, margin=1) for i in range(len(annotations))]
        for i in range(len(rectangles)):
            curr_rect = rectangles[i]
            other_rectangles = rectangles[:i] + rectangles[i + 1:]
            ellipse = Ellipse(
                center=curr_rect.anchor_point,
                width=curr_rect.width + offset_radius * 2,
                height=curr_rect.height + offset_radius * 2,
            )

            objects = lines + other_rectangles
            point_to_area = dict()
            for p in ellipse.points(resolution=100):
                curr_rect.center = p
                area = 0
                for obj in objects:
                    area += curr_rect.intersection_area(obj)
                point_to_area[p] = area
            best_point = min(point_to_area, key=point_to_area.get)

            annotations[i].anncoords = 'data'
            annotations[i].set_position((best_point.x, best_point.y))

    def _add_constraints(self):
        plot_data = self.constraints_plot_data
        for pd in plot_data:
            self.add_plot(x=pd.x, y=pd.y, color=pd.color)

    def _add_constraints_annotations(self):
        plot_data = self.constraints_plot_data
        for pd in plot_data:
            belonging_solutions = pd.get_belonging_solutions(self.solutions)
            annotated_section = pd.get_widest_section_indices(belonging_solutions)
            mid_point = (annotated_section[0] + annotated_section[1]) // 2
            mid_x = float(pd.x[mid_point])
            mid_y = float(pd.y[mid_point])
            self.add_annotation(
                text=pd.constraint.pretty_str(),
                point=Point(mid_x, mid_y),
                ha="center", va="bottom",
                text_offset=(0, 10),
                angle=pd.angle(self.aspect),
                fill_color=pd.color,
                alpha=0.3
            )

    def _add_acceptable_field_fill(self):
        acceptable_sols = filter(lambda sol: sol.is_acceptable, self.solutions)
        positions = np.asarray([(float(sol.solution[0]), float(sol.solution[1])) for sol in acceptable_sols])
        hull = ConvexHull(positions)
        hull_points = positions[hull.vertices]
        self.add_fill(x=hull_points[:, 0], y=hull_points[:, 1], color='#FFB4BB', alpha=0.9, z_order=1)

    def _add_solution_points(self):
        positions = [Point(float(sol.solution[0]), float(sol.solution[1])) for sol in self.solutions]
        self.add_points(positions, size=50, color='#BAFFC9', z_order=3)

    def _add_points_annotation(self):
        annotations = []
        positions = [Point(float(sol.solution[0]), float(sol.solution[1])) for sol in self.solutions]
        for pos, sol in zip(positions, self.solutions):
            b1 = pretty(sol.basis_variables[0])
            b2 = pretty(sol.basis_variables[1])
            b1_value = sol.solution[sol.basis[0]]
            b2_value = sol.solution[sol.basis[1]]
            label = f"Базис: \n{b1} = {b1_value}\n{b2} = {b2_value}"
            annotation = self.add_annotation(label, pos, text_offset=(0, 0), va='center',
                                             arrow_properties=dict(arrowstyle='-'), z_order=2)
            annotations.append(annotation)
        self._adjust_annotations(annotations, offset_radius=0.8)
