import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Annotation
from scipy.spatial import ConvexHull
from shapely import Point, LineString
from sympy import pretty, Rational

from report.model.report_prettifier import rational_str, expr_str
from tasks.task1_2_lp.model import BasisSolution, Constraint, LPProblem, Objective, ObjectiveType, CompOperator
from tasks.task1_2_lp.model.solvers import BruteforceSolver
from tasks.task1_2_lp.view.plot import PlotData, LinearFunction, PlotColors, AxesBounds

from tasks.task1_2_lp.view.plot.util import (AnnotationRectangle, Contur, find_intersections,
                                             filter_intersections_on_line, find_widest_line_segment)
from tasks.task1_2_lp.view.plot.plot_settings import get_plot_data


def show_lpp_plot(lpp: LPProblem, solutions: list[BasisSolution], colors: PlotColors):
    plot_data = lpp_plot_data(lpp, solutions, colors)
    plot_data.figure.show()
    plt.show()


def save_lpp_plot(lpp: LPProblem, solutions: list[BasisSolution], colors: PlotColors, path: Path):
    plot_data = lpp_plot_data(lpp, solutions, colors)
    plot_data.figure.savefig(path.as_posix(), bbox_inches='tight')


def lpp_plot_data(lpp: LPProblem, solutions: list[BasisSolution], colors: PlotColors) -> PlotData:
    if lpp.var_count != 2:
        raise ValueError("Нельзя отобразить на графике ЗЛП где количество переменных не равно 2")

    axes_bounds = AxesBounds.get_from_solutions(solutions, padding=7.0)
    plot_data = get_plot_data(figure_size=(16, 10), ax_bounds=axes_bounds)
    plot_constraints(lpp.constraints, plot_data, color=colors.constraints_color)
    plot_acceptable_field_fill(solutions, plot_data)

    opt_sol_index = [i for i in range(len(solutions)) if solutions[i].is_opt and solutions[i].is_acceptable][0]
    opt_sol = solutions[opt_sol_index]
    plot_objective(lpp.objective, opt_sol, plot_data, color=colors.objective_color)

    all_lfs = get_all_lfs(lpp.constraints, lpp.objective, opt_sol, axes_bounds)
    all_intersections = find_intersections(all_lfs)
    filtered_intersections = list(filter(plot_data.axes_bounds.contains, all_intersections))

    plot_constraints_annotations(lpp.constraints, filtered_intersections, colors.constraints_color, plot_data)
    obj_annotation_point = plot_objective_annotation(lpp.objective, opt_sol, filtered_intersections,
                                                     colors.objective_color, plot_data)
    plot_objective_arrow(lpp.objective, opt_sol, obj_annotation_point, plot_data, colors.objective_color)

    plot_solutions(solutions, plot_data, colors.solutions_color)

    annotations = plot_solution_annotations(solutions, plot_data)
    adjust_annotations(annotations, all_lfs, plot_data, offset_radius=0.8)
    return plot_data


def plot_constraints(constraints: list[Constraint], plot_data: PlotData, color: str, resolution=100):
    linear_functions = [LinearFunction.from_constraint(constraint) for constraint in constraints]
    for lf in linear_functions:
        x, y = lf.plot_values(plot_data, resolution=resolution)
        plot_data.axes.plot(x, y, color=color, linewidth=2)


def plot_objective(objective: Objective, opt_sol: BasisSolution, plot_data: PlotData, color: str, resolution=100):
    linear_function = LinearFunction.from_objective(objective, opt_sol)
    x, y = linear_function.plot_values(plot_data, resolution=resolution)
    plot_data.axes.plot(x, y, color=color, linewidth=2, linestyle='--', zorder=2)


def get_all_lfs(constraints: list[Constraint], objective: Objective, opt_sol: BasisSolution, axes_bounds: AxesBounds):
    constraint_lfs = [LinearFunction.from_constraint(c) for c in constraints]
    objective_lf = [LinearFunction.from_objective(objective, opt_sol)]
    zero_lfs = [LinearFunction(0, 1, 0), LinearFunction(1, 0, 0)]
    bounds_lfs = [LinearFunction(0, 1, axes_bounds.top_y),
                  LinearFunction(0, 1, axes_bounds.bottom_y),
                  LinearFunction(1, 0, axes_bounds.left_x),
                  LinearFunction(1, 0, axes_bounds.right_x)]

    return constraint_lfs + objective_lf + zero_lfs + bounds_lfs


def plot_constraints_annotations(
        constraints: list[Constraint],
        total_intersections: list[Point],
        color: str,
        plot_data: PlotData):
    def annotation_text(constraint: Constraint):
        coeffs = constraint.coeffs
        variables = constraint.variables
        const = constraint.const
        return f'{expr_str(coeffs, variables)} ≤ {rational_str(const)}'

    constraint_lfs = [LinearFunction.from_constraint(c) for c in constraints]
    for i, lf in enumerate(constraint_lfs):
        on_line_points = filter_intersections_on_line(lf, total_intersections)
        widest_segment = find_widest_line_segment(on_line_points)
        mid_x = (widest_segment[0].x + widest_segment[1].x) / 2
        mid_y = (widest_segment[0].y + widest_segment[1].y) / 2
        plot_data.axes.annotate(
            text=annotation_text(constraints[i]),
            xy=(mid_x, mid_y),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom',
            rotation=lf.angle(plot_data.aspect),
            rotation_mode='anchor',
            bbox=dict(boxstyle='round,pad=0.5', fc=color, ec='gray', alpha=0.5),
            fontsize=9
        )


def plot_objective_annotation(objective: Objective, opt_sol: BasisSolution, total_intersections: list[Point],
                              color: str, plot_data: PlotData):
    def annotation_text():
        coeffs = objective.coeffs
        variables = objective.variables
        const = objective.const
        func_sym = 'max' if objective.type == ObjectiveType.MAX else 'min'
        return f'{func_sym}({expr_str(coeffs, variables, const)})'

    lf = LinearFunction.from_objective(objective, opt_sol)
    on_line_points = filter_intersections_on_line(lf, total_intersections)
    widest_segment = find_widest_line_segment(on_line_points)
    mid_x = (widest_segment[0].x + widest_segment[1].x) / 2
    mid_y = (widest_segment[0].y + widest_segment[1].y) / 2

    angle = lf.angle(plot_data.aspect)
    text_offset = 10
    va = 'bottom'
    if (lf.y_coeff > 0 and objective.type == ObjectiveType.MAX or
            lf.y_coeff < 0 and objective.type == ObjectiveType.MIN):
        text_offset *= -1
        va = 'top'
    plot_data.axes.annotate(
        text=annotation_text(),
        xy=(mid_x, mid_y),
        xytext=(0, text_offset),
        textcoords='offset points',
        ha='center', va=va,
        rotation=lf.angle(plot_data.aspect),
        rotation_mode='anchor',
        bbox=dict(boxstyle='round,pad=0.5', fc=color, ec='gray', alpha=0.5),
        fontsize=9
    )
    return Point(mid_x, mid_y)


def plot_acceptable_field_fill(solutions: list[BasisSolution], plot_data: PlotData):
    lpp = solutions[0].lp_problem
    acceptable_sols = filter(lambda sol: sol.is_acceptable, solutions)
    positions = [(float(sol.solution[0]), float(sol.solution[1])) for sol in acceptable_sols]
    axes_bounds_constraint = [
        Constraint([Rational(1), Rational(0)], const=Rational(plot_data.axes_bounds.left_x).round() - 1,
                   comp_operator=CompOperator.GE),
        Constraint([Rational(1), Rational(0)], const=Rational(plot_data.axes_bounds.right_x).round() + 1,
                   comp_operator=CompOperator.LE),
        Constraint([Rational(0), Rational(1)], const=Rational(plot_data.axes_bounds.bottom_y).round() - 1,
                   comp_operator=CompOperator.GE),
        Constraint([Rational(0), Rational(1)], const=Rational(plot_data.axes_bounds.top_y).round() + 1,
                   comp_operator=CompOperator.LE),
    ]
    bound_intersections = [c1.intersection(c2) for c1 in lpp.constraints for c2 in axes_bounds_constraint if
                           len(c1.intersection(c2)) > 0]
    accepted_bi = [[float(bi[0]), float(bi[1])] for bi in bound_intersections if lpp.accept(bi)]

    total_points = np.array(positions + accepted_bi)
    hull = ConvexHull(total_points)
    hull_points = total_points[hull.vertices]
    plot_data.axes.fill(hull_points[:, 0], hull_points[:, 1], '#FFB4BB', alpha=0.9)


def plot_solutions(solutions: list[BasisSolution], plot_data: PlotData, color: str):
    solutions_num = len(solutions)
    opt_sol_index = [i for i in range(solutions_num) if solutions[i].is_opt and solutions[i].is_acceptable][0]
    x = [float(sol.solution[0]) for sol in solutions]
    y = [float(sol.solution[1]) for sol in solutions]

    def style_list(common, opt):
        return [common if i != opt_sol_index else opt for i in range(solutions_num)]

    colors = style_list(color, 'white')
    sizes = style_list(50, 70)
    edge_colors = style_list('black', 'red')
    linewidths = 1.5
    plot_data.axes.scatter(x=x, y=y, s=sizes, c=colors, linewidths=linewidths, edgecolors=edge_colors, zorder=4)


def plot_solution_annotations(solutions: list[BasisSolution], plot_data: PlotData):
    def annotation_text(_sol: BasisSolution) -> str:
        b1 = pretty(_sol.basis_variables[0])
        b2 = pretty(_sol.basis_variables[1])
        b1_value = _sol.solution[_sol.basis[0]]
        b2_value = _sol.solution[_sol.basis[1]]
        return f"Базис: \n{b1} = {rational_str(b1_value)}\n{b2} = {rational_str(b2_value)}"

    annotations = []
    points = [Point(float(sol.solution[0]), float(sol.solution[1])) for sol in solutions]
    for point, sol in zip(points, solutions):
        annotation = plot_data.axes.annotate(
            text=annotation_text(sol),
            xy=(point.x, point.y),
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='gray', alpha=0.5),
            fontsize=9,
            arrowprops=dict(arrowstyle='-')
        )
        annotations.append(annotation)
    opt_sol_index = [i for i in range(len(solutions)) if solutions[i].is_opt and solutions[i].is_acceptable][0]
    opt_point = points[opt_sol_index]
    opt_annotation = plot_data.axes.annotate(
        text='OPT',
        xy=(opt_point.x, opt_point.y),
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', fc='r', ec='gray', alpha=0.7),
        fontsize=9,
        arrowprops=dict(arrowstyle='-'),
        color='white'
    )
    annotations.append(opt_annotation)
    return annotations


def plot_objective_arrow(objective: Objective, opt_sol: BasisSolution, obj_annotation_point: Point,
                         plot_data: PlotData, color: str):
    start = obj_annotation_point

    lf = LinearFunction.from_objective(objective, opt_sol)
    angle = lf.angle(1) + 90
    if (lf.y_coeff > 0 and objective.type == ObjectiveType.MIN or
            lf.y_coeff < 0 and objective.type == ObjectiveType.MAX):
        angle += 180
    angle_rad = angle * math.pi / 180
    arrow_len = 1
    offset = 0.1
    end = Point(start.x + arrow_len * math.cos(angle_rad) * plot_data.aspect,
                start.y + arrow_len * math.sin(angle_rad) / plot_data.aspect)
    start = Point(start.x + offset * math.cos(angle_rad) * plot_data.aspect,
                  start.y + offset * math.sin(angle_rad) / plot_data.aspect)
    plot_data.axes.annotate(
        text='', xy=(end.x, end.y), xytext=(start.x, start.y),
        arrowprops=dict(width=15, headwidth=25, color=color, alpha=0.7, ec='black', zorder=1, lw=2)
    )


def adjust_annotations(annotations: list[Annotation],
                       linear_functions: list[LinearFunction],
                       plot_data: PlotData, offset_radius: float):
    def lf_to_ls(lf: LinearFunction):
        bounds = plot_data.axes_bounds
        left_y = lf.y(bounds.left_x)
        right_y = lf.y(bounds.right_x)
        if left_y is None or right_y is None:
            y0 = bounds.bottom_y
            y1 = bounds.top_y
            x0 = lf.x(y0)
            x1 = lf.x(y1)
        else:
            y0 = left_y
            y1 = right_y
            x0 = bounds.left_x
            x1 = bounds.right_x
        return LineString([[x0, y0], [x1, y1]])

    lines = [lf_to_ls(_lf) for _lf in linear_functions]
    rectangles = [AnnotationRectangle(annotations[i], plot_data.axes, margin=1.5) for i in range(len(annotations))]
    for i in range(len(rectangles)):
        curr_rect = rectangles[i]
        other_rectangles = rectangles[:i] + rectangles[i + 1:]
        contur = Contur(
            rectangle=curr_rect,
            radius=offset_radius,
        )
        objects = lines + other_rectangles
        point_to_area = dict()
        for p in contur.points(resolution=100):
            curr_rect.center = p
            area = 0
            for obj in objects:
                area += curr_rect.intersection_area(obj)
            point_to_area[p] = area
        best_point = min(point_to_area, key=point_to_area.get)

        annotations[i].anncoords = 'data'
        annotations[i].set_position((best_point.x, best_point.y))
        curr_rect.center = best_point
